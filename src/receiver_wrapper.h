/**
 * Spout receiver wrapper
 *
 * Wraps SpoutReceiver from Spout SDK with performance tracking.
 */

#pragma once

#include <string>
#include <vector>
#include <memory>
#include <tuple>
#include <chrono>

// Forward declarations for Spout SDK
class Spout;

/**
 * C++ wrapper for Spout receiver with performance monitoring.
 */
class ReceiverWrapper {
public:
    /**
     * Create a Spout receiver.
     *
     * @param sender_name Name of sender to connect to (optional)
     * @throws std::runtime_error if receiver creation fails
     */
    explicit ReceiverWrapper(const std::string& sender_name = "");

    /**
     * Destructor - releases Spout receiver resources.
     */
    ~ReceiverWrapper();

    // Disable copy (move-only type)
    ReceiverWrapper(const ReceiverWrapper&) = delete;
    ReceiverWrapper& operator=(const ReceiverWrapper&) = delete;

    /**
     * Receive texture from Spout sender.
     *
     * @param texture_id OpenGL texture ID to receive into
     * @return Tuple of (width, height) of received texture
     * @throws std::runtime_error if receive fails
     */
    std::tuple<int, int> receive_texture(unsigned int texture_id);

    /**
     * Check if new frame is available.
     *
     * @return true if sender has new frame
     */
    bool is_updated();

    /**
     * Connect to a different sender.
     *
     * @param name Name of sender to connect to
     * @throws std::runtime_error if connection fails
     */
    void select_sender(const std::string& name);

    /**
     * Get list of available Spout senders.
     *
     * @return Vector of sender names
     */
    std::vector<std::string> get_sender_list();

    /**
     * Get name of currently connected sender.
     *
     * @return Active sender name (empty if not connected)
     */
    std::string get_active_sender() const;

    /**
     * Get texture width.
     *
     * @return Width in pixels (0 if not connected)
     */
    int get_width() const;

    /**
     * Get texture height.
     *
     * @return Height in pixels (0 if not connected)
     */
    int get_height() const;

    /**
     * Get last receive latency in milliseconds.
     *
     * @return Latency in milliseconds
     */
    double get_last_receive_time_ms() const;

private:
    std::unique_ptr<Spout> m_receiver;
    std::string m_active_sender;
    int m_width;
    int m_height;
    bool m_initialized;

    // Performance tracking
    std::chrono::high_resolution_clock::time_point m_last_receive;
    double m_last_receive_time_ms;
};
