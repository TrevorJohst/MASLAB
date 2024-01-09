// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from robot_interface:msg/DriveCmd.idl
// generated code does not contain a copyright notice

#ifndef ROBOT_INTERFACE__MSG__DETAIL__DRIVE_CMD__TRAITS_HPP_
#define ROBOT_INTERFACE__MSG__DETAIL__DRIVE_CMD__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "robot_interface/msg/detail/drive_cmd__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace robot_interface
{

namespace msg
{

inline void to_flow_style_yaml(
  const DriveCmd & msg,
  std::ostream & out)
{
  out << "{";
  // member: l_speed
  {
    out << "l_speed: ";
    rosidl_generator_traits::value_to_yaml(msg.l_speed, out);
    out << ", ";
  }

  // member: r_speed
  {
    out << "r_speed: ";
    rosidl_generator_traits::value_to_yaml(msg.r_speed, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const DriveCmd & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: l_speed
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "l_speed: ";
    rosidl_generator_traits::value_to_yaml(msg.l_speed, out);
    out << "\n";
  }

  // member: r_speed
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "r_speed: ";
    rosidl_generator_traits::value_to_yaml(msg.r_speed, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const DriveCmd & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace robot_interface

namespace rosidl_generator_traits
{

[[deprecated("use robot_interface::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const robot_interface::msg::DriveCmd & msg,
  std::ostream & out, size_t indentation = 0)
{
  robot_interface::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use robot_interface::msg::to_yaml() instead")]]
inline std::string to_yaml(const robot_interface::msg::DriveCmd & msg)
{
  return robot_interface::msg::to_yaml(msg);
}

template<>
inline const char * data_type<robot_interface::msg::DriveCmd>()
{
  return "robot_interface::msg::DriveCmd";
}

template<>
inline const char * name<robot_interface::msg::DriveCmd>()
{
  return "robot_interface/msg/DriveCmd";
}

template<>
struct has_fixed_size<robot_interface::msg::DriveCmd>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<robot_interface::msg::DriveCmd>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<robot_interface::msg::DriveCmd>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // ROBOT_INTERFACE__MSG__DETAIL__DRIVE_CMD__TRAITS_HPP_
