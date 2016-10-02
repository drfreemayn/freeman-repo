#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include <QQmlContext>

#include "imageprocessing.h"

int main(int argc, char *argv[])
{
  // Create application and engine
  QGuiApplication app(argc, argv);
  QQmlApplicationEngine engine;

  // Add image provider first (required by qml)
  MyImageProvider* provider = new MyImageProvider(QQuickImageProvider::Image);
  engine.addImageProvider(QLatin1String("imgprovider"), provider);
  engine.rootContext()->setContextProperty("imgprovider", provider);

  // Load GUI from qml
  engine.load(QUrl("qrc:///qml/process-eye.qml"));

  // Find the main window in the engine and connect a signal
  // for the update image scheme
  QObject *rootObject = engine.rootObjects().first();
  QObject::connect(rootObject, SIGNAL(imageChosen(QUrl)),
                   provider, SLOT(setImage(QUrl)));

  // To access child, set propery objectName
  //QObject *qmlObject = rootObject->findChild<QObject*>("appWindow");

  return app.exec();
}