#include <WiFi.h>
#include <ArduinoHttpClient.h>

const char* ssid = "A202";         // Wi-Fi SSID
const char* password = "ssafy202";  // Wi-Fi 비밀번호

const int pirPinA = 2;                   // PIR 센서 A 핀
const int pirPinB = 3;                   // PIR 센서 B 핀
int pirStateA = LOW;
int pirStateB = LOW;
int valA = 0;
int valB = 0;

const int seniorId = 1;  

String lastDetected = "";               // 마지막 감지된 센서 ("A" 또는 "B")
unsigned long lastDetectedTime = 0;     // 마지막 감지 시간 기록 (밀리초 단위)

WiFiClient wifiClient;
HttpClient httpClient(wifiClient, "k11a202.p.ssafy.io", 8080); // 서버 IP 주소와 포트

void setup() {
  Serial.begin(9600);
  pinMode(pirPinA, INPUT);
  pinMode(pirPinB, INPUT);

  // Wi-Fi 연결
  WiFi.begin(ssid, password);
  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected to Wi-Fi");
}

void loop() {
  valA = digitalRead(pirPinA);
  valB = digitalRead(pirPinB);

  unsigned long currentTime = millis(); // 현재 시간 저장

  // A 센서가 감지되었을 때
  if (valA == HIGH && pirStateA == LOW) {
    Serial.println("Sensor A detected motion!");
    
    // 이전에 B가 감지되었다면 나감으로 판단
    if (lastDetected == "B" && (currentTime - lastDetectedTime) < 3000) { // 3초 이내에 A 감지 시 나감 판단
      sendData("/api/v1/exit/start");
    }
    
    // 마지막 감지된 센서 및 시간 업데이트
    lastDetected = "A";
    lastDetectedTime = currentTime;
    pirStateA = HIGH;
  } else if (valA == LOW && pirStateA == HIGH) {
    Serial.println("Sensor A no motion");
    pirStateA = LOW;
  }

  // B 센서가 감지되었을 때
  if (valB == HIGH && pirStateB == LOW) {
    Serial.println("Sensor B detected motion!");
    
    // 이전에 A가 감지되었다면 들어옴으로 판단
    if (lastDetected == "A" && (currentTime - lastDetectedTime) < 3000) { // 3초 이내에 B 감지 시 들어옴 판단
      sendData("/api/v1/entry/end");
    }

    // 마지막 감지된 센서 및 시간 업데이트
    lastDetected = "B";
    lastDetectedTime = currentTime;
    pirStateB = HIGH;
  } else if (valB == LOW && pirStateB == HIGH) {
    Serial.println("Sensor B no motion");
    pirStateB = LOW;
  }

  delay(500);  // 100ms 지연
}

void sendData(String endpoint) {
  if (WiFi.status() == WL_CONNECTED) {   // Wi-Fi 연결 확인
    String jsonPayload = "{\"seniorId\": " + String(seniorId) + "}"; // JSON 형식으로 숫자 1 전송

    // POST 요청 시작
    httpClient.beginRequest();
    httpClient.post(endpoint); // 동적으로 엔드포인트 설정
    httpClient.sendHeader("Content-Type", "application/json");
    httpClient.sendHeader("Content-Length", jsonPayload.length());
    httpClient.beginBody();
    httpClient.print(jsonPayload);
    httpClient.endRequest();

    // 응답 코드 확인
    int statusCode = httpClient.responseStatusCode();
    String response = httpClient.responseBody();
    Serial.print("Status code: ");
    Serial.println(statusCode);
    Serial.print("Response: ");
    Serial.println(response);
  } else {
    Serial.println("Wi-Fi Disconnected");
  }
}
