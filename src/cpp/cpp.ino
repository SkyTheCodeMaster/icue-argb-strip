#include <FastLED.h>

const int LED_PIN = 9;
const int NUM_LED = 50;

CRGB leds[NUM_LED];

void setup() {
  FastLED.addLeds<WS2812, LED_PIN, GRB>(leds, NUM_LED);
  FastLED.setMaxPowerInVoltsAndMilliamps(5,2000);
  Serial.begin(2000000);
}

void loop() {
  Serial.readBytes( (char*)leds, NUM_LED * 3);
  FastLED.show();
  delayMicroseconds(30*NUM_LED);
  Serial.write("ok");
}
