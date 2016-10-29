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
    SHARPENING = 1
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
public:

  ImageProcessor(QQuickImageProvider::ImageType);

  QImage requestImage(const QString &id, QSize *size, const QSize& requestedSize);

  Q_INVOKABLE void processImage(const FilterTypes inFilter);

  void setFilterSize(const int inSize);

public slots:
  void loadImage(const QUrl& imagePath);
  void saveImage(const QUrl& imagePath);

signals:
  void newImageSet();

private:
  QImage s_image;

  void smoothImage(const cv::Mat& inImage, cv::Mat& outImage);
  void sharpenImage(const cv::Mat& inImage, cv::Mat& outImage);
};

#endif