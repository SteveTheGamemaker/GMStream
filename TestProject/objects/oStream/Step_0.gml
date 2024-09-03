if (global.connected) {
    var surf = application_surface;
    if (surface_exists(surf)) {
        var target_width = 640;
        var target_height = 480;

        // Create a new surface with the target resolution
        var new_surf = surface_create(target_width, target_height);
        if (surface_exists(new_surf)) {
            surface_set_target(new_surf);
            draw_surface_stretched(surf, 0, 0, target_width, target_height);
            surface_reset_target();

            var buffer_size = target_width * target_height * 4; // 4 bytes per pixel (RGBA)
            var buffer = buffer_create(buffer_size, buffer_fixed, 1);

            buffer_get_surface(buffer, new_surf, 0); // Copy new surface to buffer

            // Preparing a buffer to send the size followed by the width and height, and then the actual data
            var header_buffer = buffer_create(12, buffer_fixed, 1);
            buffer_seek(header_buffer, buffer_seek_start, 0);
            buffer_write(header_buffer, buffer_u32, buffer_size); // Write buffer size
            buffer_write(header_buffer, buffer_u32, target_width); // Write surface width
            buffer_write(header_buffer, buffer_u32, target_height); // Write surface height

            // Send the header first (size, width, height)
            network_send_raw(global.socket, header_buffer, 12);

            // Then send the actual buffer containing the surface data
            network_send_raw(global.socket, buffer, buffer_size);

            // Clean up
            if (buffer_exists(header_buffer)) {
                buffer_delete(header_buffer);
            }
            if (buffer_exists(buffer)) {
                buffer_delete(buffer);
            }
            surface_free(new_surf);
        }
    }
}