#!/usr/bin/env python3
"""Kvantum widget gallery, grabbed offscreen:
    QT_QPA_PLATFORM=offscreen QT_STYLE_OVERRIDE=kvantum python3 tools/gallery.py <out.png>"""
import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QPushButton, QCheckBox,
                             QRadioButton, QLineEdit, QComboBox, QSlider, QProgressBar, QSpinBox, QTabWidget,
                             QGroupBox, QListWidget, QTreeWidget, QTreeWidgetItem, QLabel, QTextEdit)
from PyQt6.QtCore import Qt, QTimer

app = QApplication(sys.argv)
w = QWidget(); w.resize(900, 520)
root = QHBoxLayout(w)
left = QVBoxLayout(); root.addLayout(left, 1)
g = QGroupBox("Deck"); gl = QGridLayout(g); left.addWidget(g)
b1 = QPushButton("Play"); b1.setDefault(True); gl.addWidget(b1, 0, 0)
gl.addWidget(QPushButton("Rewind"), 0, 1)
d = QPushButton("Eject"); d.setEnabled(False); gl.addWidget(d, 0, 2)
c1 = QCheckBox("Tracking"); c1.setChecked(True); gl.addWidget(c1, 1, 0)
gl.addWidget(QCheckBox("Dropouts"), 1, 1)
r1 = QRadioButton("SP"); r1.setChecked(True); gl.addWidget(r1, 2, 0)
gl.addWidget(QRadioButton("LP"), 2, 1); gl.addWidget(QRadioButton("EP"), 2, 2)
e = QLineEdit(); e.setPlaceholderText("label the tape…"); gl.addWidget(e, 3, 0, 1, 3)
cb = QComboBox(); cb.addItems(["CH 03", "CH 04", "AUX"]); gl.addWidget(cb, 4, 0)
sp = QSpinBox(); sp.setValue(66); gl.addWidget(sp, 4, 1)
s = QSlider(Qt.Orientation.Horizontal); s.setValue(64); gl.addWidget(s, 5, 0, 1, 3)
pb = QProgressBar(); pb.setValue(72); gl.addWidget(pb, 6, 0, 1, 3)
t = QTextEdit(); t.setPlainText("The tape was labelled in marker.\nNobody remembers recording it."); left.addWidget(t)
tabs = QTabWidget(); root.addWidget(tabs, 1)
lw = QListWidget(); lw.addItems(["cellar_01.vhs", "cellar_02.vhs", "blood_feed_03.vhs", "static.vhs", "do_not_play.vhs", "untitled.vhs"])
lw.setCurrentRow(2)
tw = QTreeWidget(); tw.setHeaderLabels(["Tape", "Kind"])
for a, b in (("~/bloodfeed", "hub"), ("aurorae", "frame"), ("plasma", "style"), ("kvantum", "widgets")):
    it = QTreeWidgetItem([a, b]); tw.addTopLevelItem(it); QTreeWidgetItem(it, [f"{a}/README.md", "doc"])
tw.expandAll()
tabs.addTab(lw, "Tapes"); tabs.addTab(tw, "Shelf"); tabs.addTab(QLabel("…"), "Vault")
w.show()
QTimer.singleShot(400, lambda: (w.grab().save(sys.argv[1]), app.quit()))
app.exec()
