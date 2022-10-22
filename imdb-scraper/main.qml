import QtQuick 2.15
import QtQuick.Controls 2.15

ApplicationWindow {
    visible: true
    width: 300
    height: 150
    title: "IMDb Scraper"

    Button {
        anchors.centerIn: parent
        text: "Recommend"
        font.pixelSize: 24
        onClicked: imdb.open_recommended()
    }
}