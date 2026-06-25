#include <FastLED.h>

#define LED_PIN 13
#define NUM_LEDS 84

CRGB leds[NUM_LEDS];

void setup() {
    Serial.begin(9600);
    FastLED.addLeds<WS2812, LED_PIN, GRB>(leds, NUM_LEDS).setCorrection(TypicalLEDStrip);
}

void loop() {
    if (Serial.available()) {

        String str = Serial.readStringUntil('\n');

        int r, g, b, brightness;

        if (sscanf(str.c_str(), "%d %d %d %d",
                   &r, &g, &b, &brightness) == 4) {

            fill_solid(leds, NUM_LEDS, CRGB(r, g, b));

            FastLED.setBrightness(brightness);
            FastLED.show();

            Serial.println("Color updated");
        }
    }
}