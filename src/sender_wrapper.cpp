/**
 * Spout sender wrapper implementation
 */

#include "sender_wrapper.h"
#include "Spout.h"
#include <stdexcept>

SenderWrapper::SenderWrapper(const std::string& name, int width, int height)
    : m_name(name), m_width(width), m_height(height),
      m_fps(0.0), m_last_send_time_ms(0.0), m_frame_count(0) {

    if (name.empty()) {
        throw std::runtime_error("Sender name cannot be empty");
    }
    if (width <= 0 || height <= 0) {
        throw std::runtime_error("Invalid dimensions: " +
                                 std::to_string(width) + "x" +
                                 std::to_string(height));
    }

    m_sender = std::make_unique<Spout>();
    m_sender->SetSenderName(name.c_str());
    // Sender will be initialized on first SendTexture call
}

SenderWrapper::~SenderWrapper() {
    release();
}

bool SenderWrapper::send_texture(unsigned int texture_id) {
    if (texture_id == 0) {
        throw std::invalid_argument("Invalid texture ID: 0");
    }

    auto start = std::chrono::high_resolution_clock::now();

    bool success = m_sender->SendTexture(
        texture_id,
        GL_TEXTURE_2D,
        m_width,
        m_height,
        false,  // bInvert
        0       // HostFBO
    );

    auto end = std::chrono::high_resolution_clock::now();
    m_last_send_time_ms =
        std::chrono::duration<double, std::milli>(end - start).count();

    // Update FPS (simple rolling average)
    m_frame_count++;
    if (m_frame_count > 0) {
        auto time_since_start =
            std::chrono::duration<double>(end - m_last_send).count();
        if (time_since_start > 0.0) {
            m_fps = 1.0 / time_since_start;
        }
    }
    m_last_send = end;

    if (!success) {
        throw std::runtime_error("SendTexture failed");
    }

    return true;
}

void SenderWrapper::release() {
    if (m_sender) {
        m_sender->ReleaseSender();
        m_sender.reset();
    }
}

double SenderWrapper::get_fps() const {
    return m_fps;
}

double SenderWrapper::get_last_send_time_ms() const {
    return m_last_send_time_ms;
}

std::string SenderWrapper::get_name() const {
    return m_name;
}

int SenderWrapper::get_width() const {
    return m_width;
}

int SenderWrapper::get_height() const {
    return m_height;
}
