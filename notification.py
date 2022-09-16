import kivy
from jnius import autoclass

AndroidString = autoclass('java.lang.String')
PythonActivity = autoclass('org.kivy.android.PythonActivity')
NotificationBuilder = autoclass('android.app.Notification$Builder')

activity = autoclass('android.app.Activity')

Action = autoclass('android.app.Notification$Action')
Intent = autoclass('android.content.Intent')
PendingIntent = autoclass('android.app.PendingIntent')
Drawable = autoclass('android.R$drawable')
icon = Drawable.stat_notify_sync
noti = NotificationBuilder(PythonActivity.mActivity)
#noti.setDefaults(Notification.DEFAULT_ALL)
noti.setContentTitle(AndroidString('title'.encode('utf-8')))
noti.setContentText(AndroidString('message'.encode('utf-8')))
noti.setSmallIcon(icon)
noti.setAutoCancel(True)    
#noti.addAction(Action)
nm = PythonActivity.mActivity.getSystemService(PythonActivity.NOTIFICATION_SERVICE)
nm.notify(0,noti.build())
        