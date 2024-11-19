# Add project specific ProGuard rules here.
# By default, the flags in this file are appended to flags specified
# in /usr/local/Cellar/android-sdk/24.3.3/tools/proguard/proguard-android.txt
# You can edit the include path and order by changing the proguardFiles
# directive in build.gradle.
#
# For more details, see
#   http://developer.android.com/guide/developing/tools/proguard.html

# Add any project specific keep options here:

# Firebase 관련 ProGuard 설정
-keepattributes Signature
-keepattributes *Annotation*
-keep class com.google.** { *; }
-dontwarn com.google.**

# React Native 관련 ProGuard 설정
-keep class com.facebook.** { *; }
-dontwarn com.facebook.**
-keep class androidx.** { *; }
-dontwarn androidx.**
