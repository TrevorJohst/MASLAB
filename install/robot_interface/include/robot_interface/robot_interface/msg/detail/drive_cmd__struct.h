// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from robot_interface:msg/DriveCmd.idl
// generated code does not contain a copyright notice

#ifndef ROBOT_INTERFACE__MSG__DETAIL__DRIVE_CMD__STRUCT_H_
#define ROBOT_INTERFACE__MSG__DETAIL__DRIVE_CMD__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/DriveCmd in the package robot_interface.
typedef struct robot_interface__msg__DriveCmd
{
  float l_speed;
  float r_speed;
} robot_interface__msg__DriveCmd;

// Struct for a sequence of robot_interface__msg__DriveCmd.
typedef struct robot_interface__msg__DriveCmd__Sequence
{
  robot_interface__msg__DriveCmd * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} robot_interface__msg__DriveCmd__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ROBOT_INTERFACE__MSG__DETAIL__DRIVE_CMD__STRUCT_H_
