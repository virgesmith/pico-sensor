#include "pico/stdlib.h"
#include "pico/cyw43_arch.h"
#include "pico/unique_id.h"

#include <stdio.h>

// define these in secrets.c
extern char ssid[];
extern char pass[];

int main()
{
  stdio_init_all();
  if (cyw43_arch_init_with_country(CYW43_COUNTRY_UK))
  {
    printf("failed to initialise\n");
    return 1;
  }
  printf("initialised\n");

  pico_unique_board_id_t id;
  pico_get_unique_board_id(&id);
  char hostname[16] = {0};
  sprintf(hostname, "picow-%02x%02x%02x%02x", id.id[4], id.id[5], id.id[6], id.id[7]);

  cyw43_arch_enable_sta_mode(hostname);
  if (cyw43_arch_wifi_connect_timeout_ms(ssid, pass, CYW43_AUTH_WPA2_AES_PSK, 10000))
  {
    printf("failed to connect\n");
    return 1;
  }
  cyw43_arch_gpio_put(CYW43_WL_GPIO_LED_PIN, 1);
  printf("connected\n");
}