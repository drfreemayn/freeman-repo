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

        Image {
            id: mainImage
            source: img_provider_path
            cache: false
            function reload() {
                source = img_provider_path + Math.random();
            }

            MouseArea {
                anchors.fill: parent
                acceptedButtons: Qt.LeftButton
                cursorShape: Qt.PointingHandCursor
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
            }
        }
    }

    Column {
        spacing: 3
        Layout.fillHeight: true
        Layout.preferredWidth: parent.width * 0.25 - 5

        Label {
            id: brushLabel
            width: parent.width
            height: 20
            text: "Brushes"
            font.pixelSize: 16
            horizontalAlignment: Text.AlignHCenter
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

    }

}
