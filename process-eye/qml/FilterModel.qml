import QtQuick 2.7

import freeman 1.0

ListModel {
    ListElement {
        filterName: "Smoothing"
        filterType: Filter.SMOOTHING
    }
    ListElement {
        filterName: "Sharpening"
        filterType: Filter.SHARPENING
    }
}