import QtQuick 2.7

import freeman 1.0

ListModel {
    ListElement {
        text: "Smoothing"
        filterName: "Smoothing"
        filterType: Filter.SMOOTHING
    }
    ListElement {
        text: "Sharpening"
        filterName: "Sharpening"
        filterType: Filter.SHARPENING
    }
    ListElement {
        text: "Grayscale"
        filterName: "Grayscale"
        filterType: Filter.GRAYSCALE
    }
}