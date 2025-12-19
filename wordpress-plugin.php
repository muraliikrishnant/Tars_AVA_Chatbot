<?php
/**
 * Plugin Name: Ava Chatbot
 * Plugin URI: https://tarsgroup.co
 * Description: AI-powered chatbot widget for Tars Group using Google Gemini
 * Version: 1.0.0
 * Author: Tars Group
 * Author URI: https://tarsgroup.co
 * License: GPL v2 or later
 * License URI: https://www.gnu.org/licenses/gpl-2.0.html
 * Text Domain: ava-chatbot
 */

if (!defined('ABSPATH')) {
    exit; // Exit if accessed directly
}

define('AVA_CHATBOT_DIR', plugin_dir_path(__FILE__));
define('AVA_CHATBOT_URL', plugin_dir_url(__FILE__));
define('AVA_CHATBOT_VERSION', '1.0.0');

/**
 * Enqueue scripts and styles
 */
function ava_chatbot_enqueue_assets() {
    // Update these URLs to your deployed frontend and backend URLs
    $frontend_url = 'https://tars-ava-chatbot-g1qrp2b84.vercel.app'; // Change this!
    $backend_url = 'https://tars-ava-chatbot.onrender.com'; // Change this!
    
    // Enqueue frontend React app
    wp_enqueue_script(
        'ava-chatbot-app',
        $frontend_url . '/dist/index.js',
        [],
        AVA_CHATBOT_VERSION,
        true
    );
    
    // Enqueue frontend styles
    wp_enqueue_style(
        'ava-chatbot-style',
        $frontend_url . '/dist/index.css',
        [],
        AVA_CHATBOT_VERSION
    );
    
    // Pass backend URL to frontend via inline script
    wp_localize_script('ava-chatbot-app', 'avaConfig', [
        'apiUrl' => $backend_url,
        'frontendUrl' => $frontend_url
    ]);
}

add_action('wp_enqueue_scripts', 'ava_chatbot_enqueue_assets');

/**
 * Add shortcode for the chatbot
 */
function ava_chatbot_shortcode() {
    return '<div id="root"></div>';
}

add_shortcode('ava_chatbot', 'ava_chatbot_shortcode');

/**
 * Register settings page (optional)
 */
function ava_chatbot_register_settings() {
    register_setting('ava_chatbot_settings', 'ava_chatbot_frontend_url');
    register_setting('ava_chatbot_settings', 'ava_chatbot_backend_url');
    
    add_settings_section(
        'ava_chatbot_main',
        'Ava Chatbot Settings',
        'ava_chatbot_settings_callback',
        'ava_chatbot'
    );
    
    add_settings_field(
        'ava_chatbot_frontend_url',
        'Frontend URL',
        'ava_chatbot_frontend_url_callback',
        'ava_chatbot',
        'ava_chatbot_main'
    );
    
    add_settings_field(
        'ava_chatbot_backend_url',
        'Backend API URL',
        'ava_chatbot_backend_url_callback',
        'ava_chatbot',
        'ava_chatbot_main'
    );
}

add_action('admin_init', 'ava_chatbot_register_settings');

/**
 * Add admin menu
 */
function ava_chatbot_admin_menu() {
    add_menu_page(
        'Ava Chatbot',
        'Ava Chatbot',
        'manage_options',
        'ava_chatbot',
        'ava_chatbot_admin_page',
        'dashicons-format-chat'
    );
}

add_action('admin_menu', 'ava_chatbot_admin_menu');

/**
 * Admin page callback
 */
function ava_chatbot_admin_page() {
    ?>
    <div class="wrap">
        <h1><?php echo esc_html(get_admin_page_title()); ?></h1>
        <form action="options.php" method="post">
            <?php
            settings_fields('ava_chatbot_settings');
            do_settings_sections('ava_chatbot');
            submit_button();
            ?>
        </form>
        
        <hr />
        
        <h2>Usage</h2>
        <p>Add the chatbot to any page or post using the shortcode:</p>
        <code>[ava_chatbot]</code>
        
        <h2>Configuration</h2>
        <p>Update the URLs above to match your deployed frontend and backend.</p>
        <ul>
            <li><strong>Frontend URL:</strong> Your Vercel/Netlify deployment (e.g., https://ava-chatbot.vercel.app)</li>
            <li><strong>Backend API URL:</strong> Your Render/Railway/Cloud Run deployment (e.g., https://ava-backend.onrender.com)</li>
        </ul>
    </div>
    <?php
}

/**
 * Settings callbacks
 */
function ava_chatbot_settings_callback() {
    echo '<p>Configure your Ava Chatbot deployment URLs below.</p>';
}

function ava_chatbot_frontend_url_callback() {
    $value = get_option('ava_chatbot_frontend_url', 'https://YOUR_VERCEL_URL.vercel.app');
    echo '<input type="url" name="ava_chatbot_frontend_url" value="' . esc_attr($value) . '" size="50" />';
    echo '<p class="description">Enter your Vercel/Netlify frontend URL</p>';
}

function ava_chatbot_backend_url_callback() {
    $value = get_option('ava_chatbot_backend_url', 'https://YOUR_RENDER_URL.onrender.com');
    echo '<input type="url" name="ava_chatbot_backend_url" value="' . esc_attr($value) . '" size="50" />';
    echo '<p class="description">Enter your Render/Railway backend URL</p>';
}

/**
 * Plugin activation
 */
function ava_chatbot_activate() {
    // Flush rewrite rules
    flush_rewrite_rules();
}

register_activation_hook(__FILE__, 'ava_chatbot_activate');

/**
 * Plugin deactivation
 */
function ava_chatbot_deactivate() {
    // Clean up if needed
    flush_rewrite_rules();
}

register_deactivation_hook(__FILE__, 'ava_chatbot_deactivate');
