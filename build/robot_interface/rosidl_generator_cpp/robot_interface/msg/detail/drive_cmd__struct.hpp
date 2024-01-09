// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from robot_interface:msg/DriveCmd.idl
// generated code does not contain a copyright notice

#ifndef ROBOT_INTERFACE__MSG__DETAIL__DRIVE_CMD__STRUCT_HPP_
#define ROBOT_INTERFACE__MSG__DETAIL__DRIVE_CMD__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__robot_interface__msg__DriveCmd __attribute__((deprecated))
#else
# define DEPRECATED__robot_interface__msg__DriveCmd __declspec(deprecated)
#endif

namespace robot_interface
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct DriveCmd_
{
  using Type = DriveCmd_<ContainerAllocator>;

  explicit DriveCmd_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->l_speed = 0.0f;
      this->r_speed = 0.0f;
    }
  }

  explicit DriveCmd_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->l_speed = 0.0f;
      this->r_speed = 0.0f;
    }
  }

  // field types and members
  using _l_speed_type =
    float;
  _l_speed_type l_speed;
  using _r_speed_type =
    float;
  _r_speed_type r_speed;

  // setters for named parameter idiom
  Type & set__l_speed(
    const float & _arg)
  {
    this->l_speed = _arg;
    return *this;
  }
  Type & set__r_speed(
    const float & _arg)
  {
    this->r_speed = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    robot_interface::msg::DriveCmd_<ContainerAllocator> *;
  using ConstRawPtr =
    const robot_interface::msg::DriveCmd_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<robot_interface::msg::DriveCmd_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<robot_interface::msg::DriveCmd_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      robot_interface::msg::DriveCmd_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<robot_interface::msg::DriveCmd_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      robot_interface::msg::DriveCmd_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<robot_interface::msg::DriveCmd_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<robot_interface::msg::DriveCmd_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<robot_interface::msg::DriveCmd_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__robot_interface__msg__DriveCmd
    std::shared_ptr<robot_interface::msg::DriveCmd_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__robot_interface__msg__DriveCmd
    std::shared_ptr<robot_interface::msg::DriveCmd_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const DriveCmd_ & other) const
  {
    if (this->l_speed != other.l_speed) {
      return false;
    }
    if (this->r_speed != other.r_speed) {
      return false;
    }
    return true;
  }
  bool operator!=(const DriveCmd_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct DriveCmd_

// alias to use template instance with default allocator
using DriveCmd =
  robot_interface::msg::DriveCmd_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace robot_interface

#endif  // ROBOT_INTERFACE__MSG__DETAIL__DRIVE_CMD__STRUCT_HPP_
