#ifndef IMAGEPROCESSING_H
#define IMAGEPROCESSING_H

#include <QQuickImageProvider>
#include <QObject>

#include <opencv2\core.hpp>

class Filter : public QObject
{
  Q_OBJECT
public:

  Q_PROPERTY(FilterTypes filterType READ getType WRITE setType)
  Q_PROPERTY(int filterSize READ getSize WRITE setSize)

  Filter::Filter()
    : s_type(SMOOTHING), s_size(3) {}

  enum FilterTypes
  {
    SMOOTHING = 0,
    SHARPENING = 1,
    GRAYSCALE = 2,
    INVERT = 3
  };
  Q_ENUMS(FilterTypes)

  void setType(const FilterTypes inFilter)
  {
    if (inFilter != s_type)
    {
      s_type = inFilter;
    }
  }

  FilterTypes getType()
  {
    return s_type;
  }

  void setSize(const int inSize)
  {
    if (inSize != s_size)
    {
      s_size = inSize;
    }
  }

  int getSize()
  {
    return s_size;
  }

protected:
  FilterTypes s_type;
  int s_size;
};

class ImageProcessor : public Filter, public QQuickImageProvider
{
  Q_OBJECT

  int MAX_PREV_IMAGES = 10;

public:

  Q_PROPERTY(int imageIdx READ getImageIdx WRITE setImageIdx NOTIFY imageIdxChanged)

  ImageProcessor(QQuickImageProvider::ImageType);

  QImage requestImage(const QString &id, QSize *size, const QSize& requestedSize);

  Q_INVOKABLE void processImage(const FilterTypes inFilter,
                                int inMouseX = -1,
                                int inMouseY = -1);

  Q_INVOKABLE void setDisplayImageSize(const int inWidth,
                                       const int inHeight);

  Q_INVOKABLE void undoImage();
  Q_INVOKABLE void redoImage();

  Q_INVOKABLE int getImageIdx();
  Q_INVOKABLE void setImageIdx(int inIdx);

  Q_INVOKABLE int getNumImages();

public slots:
  void loadImage(const QUrl& imagePath);
  void saveImage(const QUrl& imagePath);

signals:
  void imageChanged();
  void imageIdxChanged();

private:
  QImage s_image;
  QVector<QImage> s_prevImages;
  int s_currImageIdx;
  cv::Size s_displaySize;

  void setImage(const QImage& inImage);

  bool getValidFilterRegion(const cv::Mat& inImage,
                            const cv::Point2d inPoint,
                            const int inSize,
                            cv::Rect& outRect);

  void rgb2gray(const cv::Mat& inImage, cv::Mat& outImage);
  void invertImage(const cv::Mat& inImage, cv::Mat& outImage);
  void smoothImage(const cv::Mat& inImage, const cv::Point2d inCursorPoint, cv::Mat& outImage);
  void sharpenImage(const cv::Mat& inImage, const cv::Point2d inCursorPoint, cv::Mat& outImage);
};

#endif