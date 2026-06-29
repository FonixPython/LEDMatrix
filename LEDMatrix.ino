#include <FastLED.h>

#define LED_PIN 13
#define NUM_LEDS 84

CRGB leds[NUM_LEDS];

byte displayMode = 0;
byte effectMode = 0;
int nextFrameDelay = 100;


void setup() {
    Serial.begin(9600);
    FastLED.addLeds<WS2812, LED_PIN, GRB>(leds, NUM_LEDS).setCorrection(TypicalLEDStrip);
}

void parseSerialInput(){
    String input = Serial.readStringUntil('\n');
    if (sscanf(str.c_str(), "%d %d %d %d %d",&a, &b, &c, &d, &e) == 5) {
        switch (a[0]){
            case 's':
                switch (a[1]){
                    case 'm':
                        displayMode = b;
                        break;
                    case 's':
                        switch (a[2]){
                            case 'h':
                                break;
                            case 'f':
                                break;
                        }
                        break;
                    case 'b':
                        FastLED.setBrightness(b);
                        break;
                }
                break;
            case 'f':
                fill_solid(leds, NUM_LEDS, CRGB(b,c,d));
            case 'o':
                leds[b] = CRGB(c,d,e);
            case 'e':
                switch (a[1]){
                    case 'm':
                        effectMode = b;
                    case 's':
                        nextFrameDelay = b;
                }
            case 'a':
                switch (a[1]){
                    case 's':
                        char animationBuffer[b][NUM_LEDS];
                        break;
                    case 'f':
                        char animationBuffer[b] = c;
                        break;
                    case 'w':
                        nextFrameDelay = [b];
                        break;
                }
            case 'd':
                FastLED.show();
        }
    }
}

void loop() {
    if (Serial.available()) {
        parseSerialInput();

    }
}