// process-eye.cpp : Defines the entry point for the console application.
//

#include <opencv2\imgproc\imgproc.hpp>
#include <opencv2\highgui\highgui.hpp>
#include <string>

int main()
{
	// Load eye image
	std::string eyeFilePath("D:\\Projects\\images\\eye-01.jpg");
	cv::Mat eyeImage = cv::imread(eyeFilePath);

	// Convert to gray-scale
	cv::cvtColor(eyeImage, eyeImage, CV_RGB2GRAY);
	const int NUM_IM_CHANNELS = 1;

	// Resize image
	cv::Size eyeImageSize = cv::Size(640, 480);
	cv::resize(eyeImage, eyeImage, eyeImageSize);

	// Perform edge detection
	cv::Mat eyeEdgeImage;
	int ddepth = eyeImage.depth();
	int dx = 1;
	int dy = 1;
	int kernel_size = 3;
	cv::Sobel(eyeImage, eyeEdgeImage, ddepth, dx, dy, kernel_size);
	
	// Find iris


	// Display result
	cv::imshow(eyeFilePath, eyeEdgeImage);
	(void) cv::waitKey(0);

	return 0;
}

