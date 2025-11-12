/**
 * Spout receiver wrapper implementation
 */

#include "receiver_wrapper.h"
#include "Spout.h"
#include <stdexcept>

ReceiverWrapper::ReceiverWrapper(const std::string& sender_name)
    : m_active_sender(sender_name), m_width(0), m_height(0),
      m_initialized(false), m_last_receive_time_ms(0.0) {

    m_receiver = std::make_unique<Spout>();

    if (!sender_name.empty()) {
        m_receiver->SetReceiverName(sender_name.c_str());
        m_active_sender = sender_name;
    }
}

ReceiverWrapper::~ReceiverWrapper() {
    if (m_receiver) {
        m_receiver->ReleaseReceiver();
        m_receiver.reset();
    }
}

std::tuple<int, int> ReceiverWrapper::receive_texture(unsigned int texture_id) {
    if (texture_id == 0) {
        throw std::invalid_argument("Invalid texture ID: 0");
    }

    auto start = std::chrono::high_resolution_clock::now();

    bool success = m_receiver->ReceiveTexture(
        texture_id,
        GL_TEXTURE_2D,
        false  // bInvert
    );

    unsigned int width = m_receiver->GetSenderWidth();
    unsigned int height = m_receiver->GetSenderHeight();

    auto end = std::chrono::high_resolution_clock::now();
    m_last_receive_time_ms =
        std::chrono::duration<double, std::milli>(end - start).count();

    if (success) {
        m_width = static_cast<int>(width);
        m_height = static_cast<int>(height);
        if (m_receiver->GetSenderName()) {
            m_active_sender = std::string(m_receiver->GetSenderName());
        }
        m_initialized = true;
    } else {
        throw std::runtime_error("ReceiveTexture failed");
    }

    m_last_receive = end;

    return std::make_tuple(m_width, m_height);
}

bool ReceiverWrapper::is_updated() {
    return m_receiver->IsUpdated();
}

void ReceiverWrapper::select_sender(const std::string& name) {
    if (name.empty()) {
        throw std::invalid_argument("Sender name cannot be empty");
    }

    m_receiver->SetReceiverName(name.c_str());
    m_active_sender = name;
}

std::vector<std::string> ReceiverWrapper::get_sender_list() {
    return m_receiver->GetSenderList();
}

std::string ReceiverWrapper::get_active_sender() const {
    return m_active_sender;
}

int ReceiverWrapper::get_width() const {
    return m_width;
}

int ReceiverWrapper::get_height() const {
    return m_height;
}

double ReceiverWrapper::get_last_receive_time_ms() const {
    return m_last_receive_time_ms;
}
