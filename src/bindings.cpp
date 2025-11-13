/**
 * pybind11 bindings for liru
 *
 * Exposes SenderWrapper and ReceiverWrapper C++ classes to Python.
 */

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "sender_wrapper.h"
#include "receiver_wrapper.h"

namespace py = pybind11;

PYBIND11_MODULE(_liru_core, m) {
    m.doc() = "liru C++ extension - Spout 2.007 bindings for Python";

    // SenderWrapper class
    py::class_<SenderWrapper>(m, "SenderWrapper")
        .def(py::init<const std::string&, int, int>(),
             py::arg("name"),
             py::arg("width"),
             py::arg("height"),
             "Create a Spout sender")
        .def("send_texture",
             &SenderWrapper::send_texture,
             py::arg("texture_id"),
             "Send OpenGL texture via Spout")
        .def("release",
             &SenderWrapper::release,
             "Release sender resources")
        .def("get_fps",
             &SenderWrapper::get_fps,
             "Get current FPS")
        .def("get_last_send_time_ms",
             &SenderWrapper::get_last_send_time_ms,
             "Get last send time in milliseconds")
        .def("get_name",
             &SenderWrapper::get_name,
             "Get sender name")
        .def("get_width",
             &SenderWrapper::get_width,
             "Get texture width")
        .def("get_height",
             &SenderWrapper::get_height,
             "Get texture height");

    // ReceiverWrapper class
    py::class_<ReceiverWrapper>(m, "ReceiverWrapper")
        .def(py::init<const std::string&>(),
             py::arg("sender_name") = "",
             "Create a Spout receiver")
        .def("receive_texture",
             &ReceiverWrapper::receive_texture,
             py::arg("texture_id"),
             "Receive texture from Spout sender")
        .def("is_updated",
             &ReceiverWrapper::is_updated,
             "Check if new frame is available")
        .def("select_sender",
             &ReceiverWrapper::select_sender,
             py::arg("name"),
             "Connect to a different sender")
        .def("get_sender_list",
             &ReceiverWrapper::get_sender_list,
             "Get list of available senders")
        .def("get_active_sender",
             &ReceiverWrapper::get_active_sender,
             "Get active sender name")
        .def("get_width",
             &ReceiverWrapper::get_width,
             "Get texture width")
        .def("get_height",
             &ReceiverWrapper::get_height,
             "Get texture height")
        .def("get_last_receive_time_ms",
             &ReceiverWrapper::get_last_receive_time_ms,
             "Get last receive time in milliseconds")
        .def("is_initialized",
             &ReceiverWrapper::is_initialized,
             "Check if receiver was successfully initialized")
        .def("query_sender_info",
             &ReceiverWrapper::query_sender_info,
             "Query sender dimensions without receiving frames");

    // Module version - will be overridden by Python package __init__.py
    m.attr("__version__") = "0.0.0";
}
