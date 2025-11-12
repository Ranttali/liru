/**
 * Spout sender wrapper
 *
 * Wraps SpoutSender from Spout SDK with performance tracking.
 */

#pragma once

#include <string>
#include <memory>
#include <chrono>

// Forward declarations for Spout SDK
class Spout;

/**
 * C++ wrapper for Spout sender with performance monitoring.
 */
class SenderWrapper {
public:
    /**
     * Create a Spout sender.
     *
     * @param name Unique sender name (visible to receivers)
     * @param width Texture width in pixels
     * @param height Texture height in pixels
     * @throws std::runtime_error if sender creation fails
     */
    SenderWrapper(const std::string& name, int width, int height);

    /**
     * Destructor - releases Spout sender resources.
     */
    ~SenderWrapper();

    // Disable copy (move-only type)
    SenderWrapper(const SenderWrapper&) = delete;
    SenderWrapper& operator=(const SenderWrapper&) = delete;

    /**
     * Send OpenGL texture via Spout.
     *
     * @param texture_id OpenGL texture ID
     * @return true if send succeeded
     * @throws std::runtime_error if send fails
     */
    bool send_texture(unsigned int texture_id);

    /**
     * Release sender resources.
     */
    void release();

    /**
     * Get current frames per second (rolling average).
     *
     * @return FPS as double
     */
    double get_fps() const;

    /**
     * Get last send latency in milliseconds.
     *
     * @return Latency in milliseconds
     */
    double get_last_send_time_ms() const;

    /**
     * Get sender name.
     *
     * @return Sender name
     */
    std::string get_name() const;

    /**
     * Get texture width.
     *
     * @return Width in pixels
     */
    int get_width() const;

    /**
     * Get texture height.
     *
     * @return Height in pixels
     */
    int get_height() const;

private:
    std::unique_ptr<Spout> m_sender;
    std::string m_name;
    int m_width;
    int m_height;

    // Performance tracking
    std::chrono::high_resolution_clock::time_point m_last_send;
    double m_fps;
    double m_last_send_time_ms;
    int m_frame_count;
};
