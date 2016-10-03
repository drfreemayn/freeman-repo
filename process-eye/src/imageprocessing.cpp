#include <iostream>
#include <string>

#include <opencv2/core.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>

#include <QFileInfo>

#include "imageprocessing.h"
#include "mat_and_qimage.hpp"

void processEye(cv::Mat& eyeImage, cv::Mat &outImage)
{
  // Convert to gray-scale
  cv::cvtColor(eyeImage, eyeImage, CV_RGB2GRAY);
  const int NUM_IM_CHANNELS = 1;

  // Resize image
  cv::Size eyeImageSize = cv::Size(640, 480);
  cv::resize(eyeImage, eyeImage, eyeImageSize);

  // Perform edge detection
  cv::Mat edgeImageX;
  cv::Mat edgeImageY;
  cv::Mat edgeImage;
  int kernel_size = 3;
  int scale = 1;
  int delta = 0;
  cv::Sobel(eyeImage,
    edgeImageX,
    eyeImage.depth(), // value type
    1, // x_order_deriv
    0, // y_order_deriv
    kernel_size,
    scale,
    delta,
    cv::BORDER_DEFAULT);
  cv::Sobel(eyeImage,
    edgeImageY,
    eyeImage.depth(),
    0,
    1,
    kernel_size,
    scale,
    delta,
    cv::BORDER_DEFAULT);
  addWeighted(edgeImageX, 0.5, edgeImageY, 0.5, 0, edgeImage);

  // Smooth edge image
  cv::Mat smoothedImg;
  int ksize = 9;
  cv::Size kernel(ksize, ksize);
  double sigma = 2;
  cv::GaussianBlur(edgeImage, smoothedImg, kernel, sigma);

  // Cut out ROI between corners
  cv::Point2d leftCorner(130.0, 270.0);
  cv::Point2d rightCorner(590.0, 300.0);
  cv::Rect2d irisRoi(130, 0, (590 - 130), smoothedImg.rows);
  cv::Mat irisImg = smoothedImg(irisRoi).clone();

  // Resize to something even smaller
  cv::Size resizedIrisImageSize = cv::Size(320, 240);
  cv::resize(irisImg, irisImg, resizedIrisImageSize);

  // Find eyelid edges

  // Find iris and pupil
  std::vector<cv::Vec3f> circles;
  double minDistBetweenCircles = 1;
  double accumulatorToImageRatio = 1;

  // Limit search radius to something reasonable
  int minRadius = 0.05*irisImg.rows;
  int maxRadius = 0.50*irisImg.rows;
  cv::HoughCircles(irisImg, circles, cv::HOUGH_GRADIENT, accumulatorToImageRatio, minDistBetweenCircles, 100, 50);
  for (int i = 0; i < circles.size(); i++)
  {
    cv::Point center(cvRound(circles[i][0]), cvRound(circles[i][1]));
    int radius = cvRound(circles[i][2]);
    // draw the circle center
    circle(irisImg, center, 3, cv::Scalar(255, 255, 25), -1, 8, 0);
    // draw the circle outline
    circle(irisImg, center, radius, cv::Scalar(255, 255, 255), 1, 8, 0);

    std::cout << center << std::endl;
  }

  outImage = irisImg;
}

void createSqiImage(cv::Mat& image)
{
  cv::Size imSize = cv::Size(image.cols, image.rows);

  // Create smoothed image
  const int SMOOTHING_KERNEL_SiZE = 3;
  cv::Size KERNEL_SIZE = cv::Size(SMOOTHING_KERNEL_SiZE, SMOOTHING_KERNEL_SiZE);
  cv::Mat smoothed = cv::Mat::zeros(imSize, CV_64F);
  cv::GaussianBlur(image, smoothed, KERNEL_SIZE, 0, 0);

  // Calculate SQI
  cv::Mat sqi = cv::Mat::zeros(imSize, CV_64F);
  image.convertTo(image, CV_64F);
  smoothed.convertTo(smoothed, CV_64F);
  divide(image, smoothed, sqi, CV_64F);
  for (int i = 0; i < sqi.rows; i++)
    for (int j = 0; j < sqi.cols; j++)
      if (sqi.at<double>(i, j)*0.0 != 0.0)
        sqi.at<double>(i, j) = 0;

  double min, max;
  cv::minMaxLoc(sqi, &min, &max);

  cv::normalize(sqi, sqi, 0.0, 255.0, cv::NORM_MINMAX, CV_64F);
}

MyImageProvider::MyImageProvider(QQuickImageProvider::ImageType)
  : s_image(":/eye.jpg"), QQuickImageProvider(QQuickImageProvider::Image)
{
}

QImage MyImageProvider::requestImage(const QString &id, QSize *size, const QSize& requestedSize)
{
  QImage result;

  if (requestedSize.isValid()) {
    result = s_image.scaled(requestedSize, Qt::KeepAspectRatio);
  }
  else {
    result = s_image;
  }
  *size = result.size();
  return result;
}

void MyImageProvider::loadImage(const QUrl& imagePath)
{
  s_image.load(imagePath.toLocalFile());
  emit newImageSet();
}

void MyImageProvider::saveImage(const QUrl& imagePath)
{
  s_image.save(imagePath.toLocalFile());
}

void MyImageProvider::smoothImage()
{
  cv::Mat image = ocv::qt::qimage_to_mat_cpy(s_image);
  
  // Apply smoothing
  cv::Mat smoothedImg;
  int ksize = 9;
  cv::Size kernel(ksize, ksize);
  double sigma = 3;
  cv::GaussianBlur(image, smoothedImg, kernel, sigma);

  s_image = ocv::qt::mat_to_qimage_cpy(smoothedImg);
  emit newImageSet();
}