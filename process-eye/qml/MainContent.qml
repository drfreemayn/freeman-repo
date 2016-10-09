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
            onClicked: imgprovider.processImage(imgprovider.filterType)
        }       
    }

    Column {
        spacing: 3
        Layout.fillHeight: true
        Layout.preferredWidth: parent.width * 0.25 - 5

        Label {
			id: brushLabel
            width: parent.width
            text: "Brushes"
            font.pixelSize: 16
            horizontalAlignment: Text.AlignHCenter
        }

        ListView {
            width: parent.width
			height: 0.5*parent.height
            id: listView

            Component {
                id: filterDelegate
                Button {
                    width: parent.width
                    height: parent.height / filterModel.count
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

		Item {
			width: parent.width
			height: 100
			Label {
				width: parent.width
				text: "Filter size:"
				font.pixelSize: 14
			}

			Slider {
				id: filterSizeSlider
				width: parent.width
				height: 50
				minimumValue: 3
				maximumValue: 23
				updateValueWhileDragging: false
				stepSize: 2
				onValueChanged: { imgprovider.filterSize = value; }
			}
		}
    }

}