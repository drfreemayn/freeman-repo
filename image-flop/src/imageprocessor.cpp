#include <iostream>
#include <string>

#include <opencv2/core.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>

#include <QFileInfo>

#include "imageprocessor.h"
#include "mat_and_qimage.hpp"

bool isRectInsideImage(const cv::Mat& inImage, const cv::Rect& inRect)
{
  bool valid = false;
  if ((inRect.x >= 0) && ((inRect.x + inRect.width - 1) < inImage.cols) &&
      (inRect.y >= 0) && ((inRect.y + inRect.height - 1) < inImage.rows))
  {
    valid = true;
  }
  return valid;
}

ImageProcessor::ImageProcessor(QQuickImageProvider::ImageType inType)
  : Filter(),
    QQuickImageProvider(inType),
    s_currImageIdx(0),
    s_prevImages()
{
  s_image.load(":/images/eye.jpg");
  addImageToHistory(s_image);
}

void ImageProcessor::addImageToHistory(const QImage& inImage)
{
  if (s_prevImages.size() == MAX_PREV_IMAGES)
  {
    s_prevImages.pop_back();
  }
  s_prevImages.push_front(inImage);
}

QImage ImageProcessor::requestImage(const QString &id, QSize *size, const QSize& requestedSize)
{
  QImage result;

  if (requestedSize.isValid())
  {
    result = s_image.scaled(requestedSize, Qt::KeepAspectRatio);
  }
  else
  {
    result = s_image;
  }
  *size = result.size();

  return result;
}

void ImageProcessor::setImage(const QImage& inImage)
{
  s_image = inImage.copy();
  emit imageChanged();
}

void ImageProcessor::loadImage(const QUrl& imagePath)
{
  QImage image;
  image.load(imagePath.toLocalFile());
  setImage(image);

  s_prevImages.clear();
  addImageToHistory(image);
}

void ImageProcessor::saveImage(const QUrl& imagePath)
{
  s_image.save(imagePath.toLocalFile());
}

int ImageProcessor::getImageIdx()
{
  return s_currImageIdx;
}

void ImageProcessor::setImageIdx(int inIdx)
{
  if (0 <= inIdx && inIdx < s_prevImages.size())
  {
    s_currImageIdx = inIdx;
    setImage(s_prevImages.at(s_currImageIdx));
    emit imageIdxChanged();
  }
}

void ImageProcessor::undoImage()
{
  if (s_prevImages.size() > 0 && s_currImageIdx < s_prevImages.size() - 1)
  {
    setImageIdx(++s_currImageIdx);
  }
}

void ImageProcessor::redoImage()
{
  if (s_currImageIdx > 0)
  {
    setImageIdx(--s_currImageIdx);
  }
}

int ImageProcessor::getNumImages()
{
  return s_prevImages.size();
}

cv::Rect ImageProcessor::getFilterRegion(const cv::Mat& inImage,
                                         const cv::Point2d inPoint,
                                         const int inSize)
{
  // increase by 2 since the filter creates invalid borders
  cv::Rect outRect;
  int actSize = inSize + 2;
  outRect.x = inPoint.x - (actSize - 1) / 2;
  outRect.y = inPoint.y - (actSize - 1) / 2;
  outRect.width = actSize;
  outRect.height = actSize;
  return outRect;
}

void ImageProcessor::rgb2gray(const cv::Mat& inImage, cv::Mat& outImage)
{
  if (inImage.channels() > 1)
  {
    cv::cvtColor(inImage, outImage, cv::COLOR_RGB2GRAY);
  }
  else
  {
    outImage = inImage;
  }
}

void ImageProcessor::invertImage(const cv::Mat& inImage, cv::Mat& outImage)
{
  if (inImage.channels() == 4)
  {
    cv::Mat channels[4];
    cv::split(inImage, channels);

    cv::Mat rgbArray[] = { channels[0], channels[1], channels[2] };
    cv::Mat rgbIm;
    cv::merge(rgbArray, 3, rgbIm);

    cv::bitwise_not(rgbIm, rgbIm);

    cv::Mat rgbaArray[] = { rgbIm , channels[3] };
    cv::merge(rgbaArray, 2, outImage);
  }
  else
  {
    cv::bitwise_not(inImage, outImage);
  }
}

void ImageProcessor::smoothImage(const cv::Mat& inImage, const cv::Rect& inFilterRegion, cv::Mat& outImage)
{
  cv::Size kernel(s_size, s_size);
  const double sigma = 3;
  inImage.copyTo(outImage);

  cv::Mat inputRegion = inImage(inFilterRegion);
  cv::Mat outputRegion = outImage(inFilterRegion);

  cv::GaussianBlur(inputRegion, outputRegion, kernel, sigma);
}

void ImageProcessor::sharpenImage(const cv::Mat& inImage, const cv::Rect& inFilterRegion, cv::Mat& outImage)
{
  cv::Size kernel(s_size, s_size);
  const double sigma = 3;
  const double alfa = 0.25;

  cv::Mat floatImg;
  inImage.convertTo(floatImg, CV_64FC4);

  floatImg.copyTo(outImage);
  cv::Mat inputRegion = floatImg(inFilterRegion);
  cv::Mat outputRegion = outImage(inFilterRegion);

  cv::GaussianBlur(inputRegion, outputRegion, kernel, sigma);
  cv::addWeighted(inputRegion, (1.0 + alfa), outputRegion, -alfa, 0, outputRegion);

  outImage.convertTo(outImage, CV_8UC4);
}

void ImageProcessor::scaleAndRotate(const double inScaleX,
                                    const double inScaleY,
                                    const double inAngle)
{
  cv::Mat image = ocv::qt::qimage_to_mat_cpy(s_image);

  cv::Mat scaledImage;
  cv::resize(image, scaledImage, cv::Size(0, 0), inScaleX, inScaleY);

  cv::Point2f rotCenter(scaledImage.cols/2.F, scaledImage.rows/2.F);
  cv::Mat M = cv::getRotationMatrix2D(rotCenter, inAngle, 1.0);
  cv::warpAffine(scaledImage, image, M, scaledImage.size());

  QImage newQImg = ocv::qt::mat_to_qimage_cpy(image);
  addImageToHistory(newQImg);
  setImageIdx(0);
}

void ImageProcessor::processImage(const FilterTypes inFilter,
                                  const bool inFullImage,
                                  const int inMouseX,
                                  const int inMouseY)
{
  cv::Mat image = ocv::qt::qimage_to_mat_cpy(s_image);

  // Define region to apply filter
  cv::Rect filterRegion(-1, -1, -1, -1);
  if (inFullImage)
  {
    filterRegion = cv::Rect(0, 0, image.cols, image.rows);
  }
  else
  {
    filterRegion = getFilterRegion(image, cv::Point2d(inMouseX, inMouseY), s_size);
  }

  // Apply filter
  if (isRectInsideImage(image, filterRegion))
  {
    cv::Mat newImage;
    switch (inFilter)
    {
    case SMOOTHING:
      smoothImage(image, filterRegion, newImage);
      break;
    case SHARPENING:
      sharpenImage(image, filterRegion, newImage);
      break;
    case GRAYSCALE:
      rgb2gray(image, newImage);
      break;
    case INVERT:
      invertImage(image, newImage);
      break;
    }

    QImage newQImg = ocv::qt::mat_to_qimage_cpy(newImage);
    addImageToHistory(newQImg);
    setImageIdx(0);
  }
}
