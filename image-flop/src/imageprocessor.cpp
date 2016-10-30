#include <iostream>
#include <string>

#include <opencv2/core.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>

#include <QFileInfo>

#include "imageprocessor.h"
#include "mat_and_qimage.hpp"

bool isPointInsideImage(const cv::Mat& inImage, const cv::Point2d& inCursorPoint)
{
  bool valid = false;
  if ((0 < inCursorPoint.x) && (inCursorPoint.x < (inImage.cols - 1)) &&
    (0 < inCursorPoint.y) && (inCursorPoint.y < (inImage.rows - 1)))
  {
    valid = true;
  }
  return valid;
}

bool isRectInsideImage(const cv::Mat& inImage, const cv::Rect& inRect)
{
  bool valid = false;
  if ((inRect.x > 0) && ((inRect.x + inRect.width - 1) < inImage.cols) &&
    (inRect.y > 0) && ((inRect.y + inRect.height - 1) < inImage.rows))
  {
    valid = true;
  }
  return valid;
}

cv::Point2d rescalePoint(const cv::Point2d& inPoint, const cv::Mat& inImage, const cv::Size& inDisplaySize)
{
  // rescale point to actual image coordinates
  cv::Point2d newPoint;
  newPoint.x = inPoint.x * (static_cast<double>(inImage.cols) / inDisplaySize.width);
  newPoint.y = inPoint.y * (static_cast<double>(inImage.rows) / inDisplaySize.height);
  return newPoint;
}

ImageProcessor::ImageProcessor(QQuickImageProvider::ImageType)
  : QQuickImageProvider(QQuickImageProvider::Image), Filter()
{
  s_image.load(":/eye.jpg");
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

void ImageProcessor::loadImage(const QUrl& imagePath)
{
  s_image.load(imagePath.toLocalFile());
  emit newImageSet();
}

void ImageProcessor::saveImage(const QUrl& imagePath)
{
  s_image.save(imagePath.toLocalFile());
}

void ImageProcessor::setDisplayImageSize(const int inWidth,
                                         const int inHeight)
{
  cv::Size size(inWidth, inHeight);
  s_displaySize = size;
}

bool ImageProcessor::getValidFilterRegion(const cv::Mat& inImage,
                                          const cv::Point2d inPoint,
                                          const int inSize,
                                          cv::Rect& outRect)
{
  // increase by 2 since the filter creates invalid borders
  int actSize = inSize + 2;
  outRect.x = inPoint.x - (actSize - 1) / 2;
  outRect.y = inPoint.y - (actSize - 1) / 2;
  outRect.width = actSize;
  outRect.height = actSize;

  bool valid = false;
  if (isRectInsideImage(inImage, outRect))
  {
    valid = true;
  }

  return valid;
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

void ImageProcessor::smoothImage(const cv::Mat& inImage, const cv::Point2d inCursorPoint, cv::Mat& outImage)
{
  cv::Size kernel(s_size, s_size);
  const double sigma = 3;

  if (isPointInsideImage(inImage, inCursorPoint))
  {
    cv::Rect region;
    bool valid = getValidFilterRegion(inImage, inCursorPoint, s_size, region);

    inImage.copyTo(outImage);
    cv::Mat inputRegion = inImage(region);
    cv::Mat outputRegion = outImage(region);

    cv::GaussianBlur(inputRegion, outputRegion, kernel, sigma);
  }
  else
  {
    cv::GaussianBlur(inImage, outImage, kernel, sigma); // apply to full image
  }
}

void ImageProcessor::sharpenImage(const cv::Mat& inImage, const cv::Point2d inCursorPoint, cv::Mat& outImage)
{
  cv::Size kernel(s_size, s_size);
  const double sigma = 3;
  const double alfa = 0.25;

  cv::Mat floatImg;
  inImage.convertTo(floatImg, CV_64FC4);

  cv::Mat smoothImage;
  if (isPointInsideImage(inImage, inCursorPoint))
  {
    cv::Rect region;
    bool valid = getValidFilterRegion(inImage, inCursorPoint, s_size, region);

    floatImg.copyTo(outImage);
    cv::Mat inputRegion = floatImg(region);
    cv::Mat outputRegion = outImage(region);

    cv::GaussianBlur(inputRegion, smoothImage, kernel, sigma);
    cv::addWeighted(inputRegion, (1.0 + alfa), smoothImage, -alfa, 0, outputRegion);
  }
  else
  {
    cv::GaussianBlur(floatImg, smoothImage, kernel, sigma);
    cv::addWeighted(floatImg, (1.0 + alfa), smoothImage, -alfa, 0, outImage);
  }

  outImage.convertTo(outImage, CV_8UC4);
}

void ImageProcessor::processImage(const FilterTypes inFilter, int inMouseX, int inMouseY)
{
  cv::Mat image = ocv::qt::qimage_to_mat_cpy(s_image);

  cv::Point2d clickedPoint(inMouseX, inMouseY);
  cv::Point2d actualPoint = rescalePoint(clickedPoint, image, s_displaySize);

  cv::Mat newImage;
  switch (inFilter)
  {
    case SMOOTHING:
      smoothImage(image, actualPoint, newImage);
      break;
    case SHARPENING:
      sharpenImage(image, actualPoint, newImage);
      break;
    case GRAYSCALE:
      rgb2gray(image, newImage);
      break;
    case INVERT:
      invertImage(image, newImage);
      break;
  }

  s_image = ocv::qt::mat_to_qimage_cpy(newImage);
  emit newImageSet();
}