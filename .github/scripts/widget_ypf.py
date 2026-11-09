from pathlib import Path

base = Path("app/src/main")
java = base / "java/com/relojypf/vintage"
xml = base / "res/xml"
layout = base / "res/layout"
drawable = base / "res/drawable"

for p in (java, xml, layout, drawable):
    p.mkdir(parents=True, exist_ok=True)

(java / "RelojWidget.java").write_text(r'''
package com.relojypf.vintage;

import android.app.PendingIntent;
import android.appwidget.AppWidgetManager;
import android.appwidget.AppWidgetProvider;
import android.content.Context;
import android.content.Intent;
import android.widget.RemoteViews;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;

public class RelojWidget extends AppWidgetProvider {
    @Override
    public void onUpdate(Context context, AppWidgetManager manager, int[] ids) {
        for (int id : ids) {
            RemoteViews views = new RemoteViews(context.getPackageName(), R.layout.widget_ypf);
            String hora = new SimpleDateFormat("HH:mm", Locale.getDefault()).format(new Date());
            views.setTextViewText(R.id.widget_hora, hora);
            Intent intent = new Intent(context, MainActivity.class);
            PendingIntent pending = PendingIntent.getActivity(
                context, 0, intent, PendingIntent.FLAG_IMMUTABLE | PendingIntent.FLAG_UPDATE_CURRENT);
            views.setOnClickPendingIntent(R.id.widget_hora, pending);
            manager.updateAppWidget(id, views);
        }
    }
}
''')

(xml / "reloj_widget_info.xml").write_text('''<?xml version="1.0" encoding="utf-8"?>
<appwidget-provider xmlns:android="http://schemas.android.com/apk/res/android"
    android:minWidth="180dp"
    android:minHeight="100dp"
    android:updatePeriodMillis="1800000"
    android:initialLayout="@layout/widget_ypf"
    android:resizeMode="horizontal|vertical"
    android:widgetCategory="home_screen" />
''')

(drawable / "widget_fondo.xml").write_text('''<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android">
    <gradient android:startColor="#FFF0CC" android:endColor="#C99E64" android:angle="270"/>
    <corners android:radius="14dp"/>
    <stroke android:width="3dp" android:color="#80502C"/>
</shape>
''')

layout.joinpath("widget_ypf.xml").write_text('''<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:gravity="center"
    android:padding="10dp"
    android:background="@drawable/widget_fondo">
    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="YPF  •  RELOJ VINTAGE"
        android:textSize="13sp"
        android:textStyle="bold"
        android:textColor="#493019"/>
    <TextView
        android:id="@+id/widget_hora"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="6dp"
        android:background="#161616"
        android:paddingLeft="14dp"
        android:paddingRight="14dp"
        android:paddingTop="4dp"
        android:paddingBottom="4dp"
        android:text="00:00"
        android:textColor="#FFF0D2"
        android:textSize="38sp"
        android:textStyle="bold"
        android:fontFamily="monospace"/>
</LinearLayout>
''')

manifest = base / "AndroidManifest.xml"
s = manifest.read_text()
receiver = '''
        <receiver android:name=".RelojWidget" android:exported="true">
            <intent-filter>
                <action android:name="android.appwidget.action.APPWIDGET_UPDATE"/>
            </intent-filter>
            <meta-data android:name="android.appwidget.provider"
                android:resource="@xml/reloj_widget_info"/>
        </receiver>
'''
if 'android:name=".RelojWidget"' not in s:
    s = s.replace("</application>", receiver + "</application>")
    manifest.write_text(s)

print("WIDGET YPF PREPARADO")
