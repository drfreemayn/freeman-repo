// application.cpp : Defines the entry point for the console application.
//

#include <iostream>
#include <string>
#include <opencv2/core.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>

using namespace cv;

cv::Mat eyeImage;

/**
* @brief makeCanvas Makes composite image from the given images
* @param vecMat Vector of Images.
* @param windowHeight The height of the new composite image to be formed.
* @param nRows Number of rows of images. (Number of columns will be calculated
*              depending on the value of total number of images).
* @return new composite image.
*/
cv::Mat makeCanvas(std::vector<cv::Mat>& vecMat, int windowHeight, int nRows) {
	int N = vecMat.size();
	nRows = nRows > N ? N : nRows;
	int edgeThickness = 10;
	int imagesPerRow = ceil(double(N) / nRows);
	int resizeHeight = floor(2.0 * ((floor(double(windowHeight - edgeThickness) / nRows)) / 2.0)) - edgeThickness;
	int maxRowLength = 0;

	std::vector<int> resizeWidth;
	for (int i = 0; i < N;) {
		int thisRowLen = 0;
		for (int k = 0; k < imagesPerRow; k++) {
			double aspectRatio = double(vecMat[i].cols) / vecMat[i].rows;
			int temp = int(ceil(resizeHeight * aspectRatio));
			resizeWidth.push_back(temp);
			thisRowLen += temp;
			if (++i == N) break;
		}
		if ((thisRowLen + edgeThickness * (imagesPerRow + 1)) > maxRowLength) {
			maxRowLength = thisRowLen + edgeThickness * (imagesPerRow + 1);
		}
	}
	int windowWidth = maxRowLength;
	cv::Mat canvasImage(windowHeight, windowWidth, CV_8UC3, Scalar(0, 0, 0));

	for (int k = 0, i = 0; i < nRows; i++) {
		int y = i * resizeHeight + (i + 1) * edgeThickness;
		int x_end = edgeThickness;
		for (int j = 0; j < imagesPerRow && k < N; k++, j++) {
			int x = x_end;
			cv::Rect roi(x, y, resizeWidth[k], resizeHeight);
			cv::Size s = canvasImage(roi).size();
			// change the number of channels to three
			cv::Mat target_ROI(s, vecMat[k].type());
			cv::resize(vecMat[k], target_ROI, s);
			if (target_ROI.type() != canvasImage.type()) {
				target_ROI.convertTo(target_ROI, canvasImage.type());
			}
			target_ROI.copyTo(canvasImage(roi));
			x_end += resizeWidth[k] + edgeThickness;
		}
	}
	return canvasImage;
}

void onMouse(int event, int x, int y, int flags, void* param)
{
  char text[100];
  //Mat img2, img3;

  //img2 = eyeImage.clone();

  if (event == CV_EVENT_LBUTTONDOWN)
  {
    std::cout << "x:" << x << " y: " << y << std::endl;
  }  

  //putText(img2, text, Point(5, 15), FONT_HERSHEY_PLAIN, 1.0, CV_RGB(0, 255, 0));
  //imshow("images", img2);
}

void processEye(cv::Mat &outImage)
{
	// Load eye image
	std::string eyeFilePath("C:/fredrikw/git/freeman-repo/process-eye/eye-01.jpg");
	cv::Mat eyeImage = cv::imread(eyeFilePath);

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
            BORDER_DEFAULT);
  cv::Sobel(eyeImage,
            edgeImageY,
            eyeImage.depth(),
            0,
            1,
            kernel_size,
            scale,
            delta,
            BORDER_DEFAULT);
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
  std::vector<Vec3f> circles;
  double minDistBetweenCircles = 1;
  double accumulatorToImageRatio = 1;

  // Limit search radius to something reasonable
  int minRadius = 0.05*irisImg.rows;
  int maxRadius = 0.50*irisImg.rows;
  cv::HoughCircles(irisImg, circles, HOUGH_GRADIENT, accumulatorToImageRatio, minDistBetweenCircles, 100, 50);
  for (int i = 0; i < circles.size(); i++)
  {
    Point center(cvRound(circles[i][0]), cvRound(circles[i][1]));
    int radius = cvRound(circles[i][2]);
    // draw the circle center
    circle(irisImg, center, 3, Scalar(255, 255, 25), -1, 8, 0);
    // draw the circle outline
    circle(irisImg, center, radius, Scalar(255, 255, 255), 1, 8, 0);

    std::cout << center << std::endl;
  }

  outImage = irisImg;
}

void createSqiImage()
{
  // Read image
  std::string imName = "shadowed_face.jpg";
  Mat image;
  image = imread(imName);
  Size imSize = Size(image.cols, image.rows);

  // Create smoothed image
  const int SMOOTHING_KERNEL_SiZE = 3;
  Size KERNEL_SIZE = Size(SMOOTHING_KERNEL_SiZE, SMOOTHING_KERNEL_SiZE);
  Mat smoothed = Mat::zeros(imSize, CV_64F);
  GaussianBlur(image, smoothed, KERNEL_SIZE, 0, 0);

  // Calculate SQI
  Mat sqi = Mat::zeros(imSize, CV_64F);
  image.convertTo(image, CV_64F);
  smoothed.convertTo(smoothed, CV_64F);
  divide(image, smoothed, sqi, CV_64F);
  for (int i = 0; i < sqi.rows; i++)
	  for (int j = 0; j < sqi.cols; j++)
		  if (sqi.at<double>(i, j)*0.0 != 0.0)
			  sqi.at<double>(i, j) = 0;

  double min, max;
  cv::minMaxLoc(sqi, &min, &max);

  normalize(sqi, sqi, 0.0, 255.0, NORM_MINMAX, CV_64F);
}

int main()
{
  processEye(eyeImage);

	// Create a canvas image
	std::vector<cv::Mat> imageVector;
	imageVector.push_back(eyeImage);

	//cv::Mat canvasImage = makeCanvas(imageVector, eyeImage.rows, 1);
  std::string windowName = "images";
  namedWindow(windowName);
  setMouseCallback(windowName, onMouse, 0);

	// Display
	imshow(windowName, eyeImage);
	waitKey(0);
}