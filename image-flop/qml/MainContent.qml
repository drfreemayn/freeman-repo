import QtQuick 2.7
import QtQuick.Controls 1.4
import QtQuick.Layouts 1.3

RowLayout {
    spacing: 5
    anchors.fill: parent
    anchors.margins: 2

    Connections {
        target: imgprovider
        onNewImageSet: mainImage.reload();
    }

    Image {
        id: mainImage
        source: "image://imgprovider/foobar"
        cache: false
        Layout.fillWidth: true
        Layout.fillHeight: true
        function reload() {
            var oldSource = source;
            source = "";
            source = oldSource;
        }

        MouseArea {
            anchors.fill: parent
            acceptedButtons: Qt.LeftButton
            cursorShape: Qt.PointingHandCursor
            onClicked: {
                imgprovider.setDisplayImageSize(parent.width, parent.height);
                imgprovider.processImage(imgprovider.filterType, mouseX, mouseY);
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
                id: filterLabel
                width: parent.width
                text: "Filter size:"
                font.pixelSize: 14
            }

            Slider {
                id: filterSizeSlider
                width: parent.width
                anchors.top: filterLabel.bottom

                minimumValue: 3
                maximumValue: 23
                updateValueWhileDragging: false
                stepSize: 2
                onValueChanged: { imgprovider.filterSize = value; }
            }
        }

        ListView {
            width: parent.width
            height: 150
            id: listView

            Component {
                id: filterDelegate
                Button {
                    id: brushButton
                    width: parent.width
                    height: 50
                    text: filterName
                    onClicked: {
                        listView.currentIndex = index;
                        imgprovider.filterType = filterType;
                    }
                }
            }

            model: FilterModel { id: filterModel }
            delegate: filterDelegate
            focus: true
        }

    }

}