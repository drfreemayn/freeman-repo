#include <iostream>
#include <string>

#include <opencv2/core.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>

#include <QFileInfo>

#include "imageprocessor.h"
#include "mat_and_qimage.hpp"

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

void ImageProcessor::smoothImage(const cv::Mat& inImage, cv::Mat& outImage)
{
  cv::Size kernel(s_size, s_size);
  double sigma = 3;
  cv::GaussianBlur(inImage, outImage, kernel, sigma);
}

void ImageProcessor::sharpenImage(const cv::Mat& inImage, cv::Mat& outImage)
{
  cv::Mat floatImg;
  inImage.convertTo(floatImg, CV_64FC4);

  double sigma = 3;
  cv::Mat smoothImage;
  cv::GaussianBlur(floatImg, smoothImage, cv::Size(s_size, s_size), sigma);

  double alfa = 0.25;
  cv::addWeighted(floatImg, (1.0+alfa), smoothImage, -alfa, 0, outImage);

  outImage.convertTo(outImage, CV_8UC4);
}

void ImageProcessor::processImage(const FilterTypes inFilter)
{
  cv::Mat image = ocv::qt::qimage_to_mat_cpy(s_image);

  cv::Mat newImage;
  switch (inFilter)
  {
    case SMOOTHING:
      smoothImage(image, newImage);
      break;
    case SHARPENING:
      sharpenImage(image, newImage);
      break;
    case GRAYSCALE:
      rgb2gray(image, newImage);
  }

  s_image = ocv::qt::mat_to_qimage_cpy(newImage);
  emit newImageSet();
}