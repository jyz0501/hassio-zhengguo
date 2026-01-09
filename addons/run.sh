Heat#!/usr/bin/env bashio

set -e

bashio::log.info "========================================="
bashio::log.info "Zinguo Bathroom Heater Add-on Starting"
bashio::log.info "========================================="

# Create custom_components directory if it doesn't exist
if [ ! -d "/config/custom_components" ]; then
    bashio::log.info "Creating custom_components directory..."
    mkdir -p /config/custom_components
fi

# Copy custom component
bashio::log.info "Installing Zinguo custom component..."
if [ -d "/usr/src/app/custom_components/zinguo" ]; then
    cp -r /usr/src/app/custom_components/zinguo /config/custom_components/
    bashio::log.success "✓ Custom component copied successfully"
    
    # Set correct permissions
    chmod -R 755 /config/custom_components/zinguo
    
    bashio::log.info ""
    bashio::log.info "Installation complete!"
    bashio::log.info "Please follow these steps:"
    bashio::log.info "1. Go to Home Assistant"
    bashio::log.info "2. Navigate to Settings → Devices & Services"
    bashio::log.info "3. Click 'Add Integration'"
    bashio::log.info "4. Search for 'Zinguo Bathroom Fan'"
    bashio::log.info "5. Enter your credentials"
    bashio::log.info ""
    bashio::log.info "Note: You may need to restart Home Assistant for the"
    bashio::log.info "integration to appear in the integration list."
    
else
    bashio::log.error "✗ Custom component not found in /usr/src/app/custom_components/"
    exit 1
fi

# Keep container running
bashio::log.info "Add-on is running. Press Ctrl+C to stop."
exec tail -f /dev/null
