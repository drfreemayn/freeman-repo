import QtQuick 2.7
import QtQuick.Controls 1.4
import QtQuick.Layouts 1.3

RowLayout {
    spacing: 5
    anchors.fill: parent
    anchors.margins: 2

    property string img_provider_path: "image://imgprovider/foobar";

    Connections {
        target: imgprovider
        onImageChanged: mainImage.reload();
    }

    ScrollView {
        Layout.fillWidth: true
        Layout.fillHeight: true
        id: scrollImage

        flickableItem.interactive: true

        Image {
            id: mainImage
            source: img_provider_path
            cache: false
            function reload() {
                source = img_provider_path + Math.random();
            }

            MouseArea {
                id: mainMouseArea
                anchors.fill: parent
                acceptedButtons: Qt.LeftButton
                cursorShape: Qt.OpenHandCursor
                enabled: false

                onClicked: {
                    imgprovider.processImage(imgprovider.filterType, false, mouseX, mouseY);
                }
                // TODO: Fix to time-based method, apply at 30 FPS if pressed.
                onPositionChanged:
                {
                  if (pressed)
                  {
                    imgprovider.processImage(imgprovider.filterType, false, mouseX, mouseY);
                  }
                }
                onWheel: {
                    if (zoomButton.checked)
                    {
                        if (wheel.modifiers & Qt.ControlModifier) {
                            mainImage.rotation += wheel.angleDelta.y / 120 * 5;
                            if (Math.abs(photoFrame.rotation) < 4)
                                mainImage.rotation = 0;
                        } else {
                            mainImage.rotation += wheel.angleDelta.x / 120;
                            if (Math.abs(mainImage.rotation) < 0.6)
                                mainImage.rotation = 0;
                            var scaleBefore = mainImage.scale;
                            mainImage.scale += mainImage.scale * wheel.angleDelta.y / 120 / 10;
                        }
                    }
                }
            }

        }
    }

    Column {
        spacing: 3
        Layout.fillHeight: true
        Layout.preferredWidth: 150

        Label {
            id: toolsLabel
            width: parent.width
            height: 20
            text: "Tools"
            font.pixelSize: 16
            horizontalAlignment: Text.AlignHCenter
        }

        RowLayout {
            width: parent.width
            height: 50
            spacing: 5

            Button {
                id: brushButton
                Image {
                    anchors.fill: parent
                    source: "qrc:/images/brush.png"
                }
                checkable: true
                Layout.fillHeight: true
                Layout.fillWidth: true

                onCheckedChanged: {
                    if (checked)
                    {
                        zoomButton.checked = false;
                        mainMouseArea.cursorShape = Qt.PointingHandCursor;
                    }
                    else
                    {
                        mainMouseArea.cursorShape = Qt.OpenHandCursor;
                    }

                    mainMouseArea.enabled = !mainMouseArea.enabled;
                    scrollImage.flickableItem.interactive = !scrollImage.flickableItem.interactive;
                }
            }

            Button {
                id: zoomButton
                Image {
                    anchors.fill: parent
                    source: "qrc:/images/magnifier.png"
                }
                checkable: true
                Layout.fillHeight: true
                Layout.fillWidth: true

                onCheckedChanged: {
                    if (checked)
                    {
                        brushButton.checked = false;
                        mainMouseArea.cursorShape = Qt.CrossCursor;
                    }
                    else
                    {
                        mainMouseArea.cursorShape = Qt.OpenHandCursor;
                    }

                    mainMouseArea.enabled = !mainMouseArea.enabled;
                    scrollImage.flickableItem.interactive = !scrollImage.flickableItem.interactive;
                }
            }
        }

        Item {
            width: parent.width
            height: 50
            Label {
                id: filterTypeLabel
                text: "Filter type:"
                font.pixelSize: 14
            }

            ComboBox {
                width: parent.width
                anchors.top: filterTypeLabel.bottom
                model: FilterModel {}
                onCurrentIndexChanged: {
                  imgprovider.filterType = model.get(currentIndex).filterType
                }
            }
        }

        Item {
            width: parent.width
            height: 50
            Label {
                id: filterSizeLabel
                text: "Filter size:"
                font.pixelSize: 14
            }

            Slider {
                id: filterSizeSlider
                width: parent.width
                anchors.top: filterSizeLabel.bottom

                minimumValue: 3
                maximumValue: 23
                updateValueWhileDragging: false
                stepSize: 2
                onValueChanged: { imgprovider.filterSize = value; }
            }
        }
    }
}
