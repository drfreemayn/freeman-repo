#ifndef IMAGEPROCESSING_H
#define IMAGEPROCESSING_H

#include <QQuickImageProvider>
#include <QObject>

class MyImageProvider : public QObject, public QQuickImageProvider
{
  Q_OBJECT

public:
  MyImageProvider(QQuickImageProvider::ImageType);

  QImage requestImage(const QString &id, QSize *size, const QSize& requestedSize);

  Q_INVOKABLE void smoothImage();
 
public slots:
  void setImage(const QUrl& imagePath);

signals:
  void newImageSet();

private:
  QImage s_image;

};

#endif