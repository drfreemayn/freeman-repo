#include <QtQml>
#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include <QQmlContext>

#include "imageprocessor.h"

int main(int argc, char *argv[])
{
  // Create application and engine
  QGuiApplication app(argc, argv);
  QQmlApplicationEngine engine;

  // Add image provider first (required by qml)
  ImageProcessor* provider = new ImageProcessor(QQuickImageProvider::Image);
  engine.addImageProvider(QLatin1String("imgprovider"), provider);
  engine.rootContext()->setContextProperty("imgprovider", provider);

  qmlRegisterType<Filter>("freeman", 1, 0, "Filter");

  // Load GUI from qml
  engine.load(QUrl("qrc:///qml/image-flop.qml"));

  // Find the main window in the engine and connect a signal
  // for the update image scheme
  QObject *rootObject = engine.rootObjects().first();
  QObject::connect(rootObject, SIGNAL(loadImageChosen(QUrl)),
                   provider, SLOT(loadImage(QUrl)));
  QObject::connect(rootObject, SIGNAL(saveImageChosen(QUrl)),
                   provider, SLOT(saveImage(QUrl)));

  // To access child, set propery objectName
  //QObject *qmlObject = rootObject->findChild<QObject*>("appWindow");

  return app.exec();
}