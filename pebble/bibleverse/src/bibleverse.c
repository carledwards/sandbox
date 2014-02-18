#include <pebble.h>

static Window *window;
static TextLayer *verse_layer;

static ScrollLayer *scroll_layer;

static const int vert_scroll_text_padding = 4;

static char verse[300];

enum {
  BIBLE_VERSE_KEY_VERSE = 0x01
};

static void window_load(Window *window) {
  Layer *window_layer = window_get_root_layer(window);
  GRect bounds = layer_get_bounds(window_layer);
  GRect max_text_bounds = GRect(0, 0, bounds.size.w, 2000);

  // Initialize the scroll layer
  scroll_layer = scroll_layer_create(bounds);

  // This binds the scroll layer to the window so that up and down map to scrolling
  scroll_layer_set_click_config_onto_window(scroll_layer, window);

  verse_layer = text_layer_create(max_text_bounds);
  text_layer_set_text(verse_layer, "Loading...");
  text_layer_set_font(verse_layer, fonts_get_system_font(FONT_KEY_GOTHIC_24_BOLD));

  // Trim text layer and scroll content to fit text box
  GSize max_size = text_layer_get_content_size(verse_layer);
  text_layer_set_size(verse_layer, max_size);
  scroll_layer_set_content_size(scroll_layer, GSize(max_size.w, max_size.h + vert_scroll_text_padding));

  // Add the layers for display
   scroll_layer_add_child(scroll_layer, text_layer_get_layer(verse_layer));

   layer_add_child(window_layer, scroll_layer_get_layer(scroll_layer));
}

static void in_received_handler(DictionaryIterator *iter, void *context) {
  Tuple *verse_tuple = dict_find(iter, BIBLE_VERSE_KEY_VERSE);

  if (verse_tuple) {
    strncpy(verse, verse_tuple->value->cstring, 300);
    text_layer_set_text(verse_layer, verse);
    GSize max_size = text_layer_get_content_size(verse_layer);
    text_layer_set_size(verse_layer, max_size);
    scroll_layer_set_content_size(scroll_layer, GSize(max_size.w, max_size.h + vert_scroll_text_padding));
  }
}

static void app_message_init(void) {
  // Register message handlers
  app_message_register_inbox_received(in_received_handler);
  // Init buffers
  app_message_open(300, 64);
}

static void window_unload(Window *window) {
  text_layer_destroy(verse_layer);
}

static void init(void) {
  window = window_create();
  app_message_init();
  window_set_window_handlers(window, (WindowHandlers) {
    .load = window_load,
    .unload = window_unload,
  });
  const bool animated = true;
  window_stack_push(window, animated);
}

static void deinit(void) {
  window_destroy(window);
}

int main(void) {
  init();

  APP_LOG(APP_LOG_LEVEL_DEBUG, "Done initializing, pushed window: %p", window);

  app_event_loop();
  deinit();
}
