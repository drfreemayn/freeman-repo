import QtQuick.Controls 1.4
import QtQuick 2.2
import QtQuick.Dialogs 1.0
import QtQuick.Layouts 1.3

ApplicationWindow 
{
    id: appWindow
    title: "Eye processing"
    height: 500
    width: 800
    visible: true

	signal loadImageChosen(url path)
	signal saveImageChosen(url path)

	FileDialog {
		id: loadImageDialog
		title: "Open file"
		folder: shortcuts.home
		nameFilters: ["Image files (*.jpg *.png)"]
		onAccepted: {
			appWindow.loadImageChosen(loadImageDialog.fileUrl);
		}
	}

	FileDialog {
		id: saveImageDialog
		title: "Save file"
		folder: shortcuts.home
		selectExisting: false
		nameFilters: ["Image files (*.jpg *.png)"]
		onAccepted: {
			appWindow.saveImageChosen(saveImageDialog.fileUrl);
		}
	}
	
	menuBar: MenuBar {
        Menu {
            title: "File"
            MenuItem {
				text: "Open image"
				onTriggered: loadImageDialog.open()
			}
			MenuItem {
				text: "Save image as..."
				onTriggered: saveImageDialog.open()
			}
            MenuItem { 
				text: "Exit"
				onTriggered: Qt.quit()
			}
        }
	}

	RowLayout {
		id: mainContent
		spacing: 5
		anchors.fill: parent
		anchors.margins: 2

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
		}

		Column {
			spacing: 3
			Layout.fillHeight: true
			Layout.preferredWidth: parent.width * 0.25 - 5
			Button {
			    width: parent.width
				height: parent.height/5
				text: "Smooth"
				onClicked: imgprovider.smoothImage()
			}
			Button {
				width: parent.width
				height: parent.height/5
				text: "Sharpen"
			}
		}

		Connections {
			target: imgprovider
			onNewImageSet: mainImage.reload(); 
		}
	}

}