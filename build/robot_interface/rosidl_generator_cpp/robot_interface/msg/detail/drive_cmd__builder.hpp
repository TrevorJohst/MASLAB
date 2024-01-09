// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from robot_interface:msg/DriveCmd.idl
// generated code does not contain a copyright notice

#ifndef ROBOT_INTERFACE__MSG__DETAIL__DRIVE_CMD__BUILDER_HPP_
#define ROBOT_INTERFACE__MSG__DETAIL__DRIVE_CMD__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "robot_interface/msg/detail/drive_cmd__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace robot_interface
{

namespace msg
{

namespace builder
{

class Init_DriveCmd_r_speed
{
public:
  explicit Init_DriveCmd_r_speed(::robot_interface::msg::DriveCmd & msg)
  : msg_(msg)
  {}
  ::robot_interface::msg::DriveCmd r_speed(::robot_interface::msg::DriveCmd::_r_speed_type arg)
  {
    msg_.r_speed = std::move(arg);
    return std::move(msg_);
  }

private:
  ::robot_interface::msg::DriveCmd msg_;
};

class Init_DriveCmd_l_speed
{
public:
  Init_DriveCmd_l_speed()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_DriveCmd_r_speed l_speed(::robot_interface::msg::DriveCmd::_l_speed_type arg)
  {
    msg_.l_speed = std::move(arg);
    return Init_DriveCmd_r_speed(msg_);
  }

private:
  ::robot_interface::msg::DriveCmd msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::robot_interface::msg::DriveCmd>()
{
  return robot_interface::msg::builder::Init_DriveCmd_l_speed();
}

}  // namespace robot_interface

#endif  // ROBOT_INTERFACE__MSG__DETAIL__DRIVE_CMD__BUILDER_HPP_
