// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from robot_interface:msg/DriveCmd.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "robot_interface/msg/detail/drive_cmd__rosidl_typesupport_introspection_c.h"
#include "robot_interface/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "robot_interface/msg/detail/drive_cmd__functions.h"
#include "robot_interface/msg/detail/drive_cmd__struct.h"


#ifdef __cplusplus
extern "C"
{
#endif

void robot_interface__msg__DriveCmd__rosidl_typesupport_introspection_c__DriveCmd_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  robot_interface__msg__DriveCmd__init(message_memory);
}

void robot_interface__msg__DriveCmd__rosidl_typesupport_introspection_c__DriveCmd_fini_function(void * message_memory)
{
  robot_interface__msg__DriveCmd__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember robot_interface__msg__DriveCmd__rosidl_typesupport_introspection_c__DriveCmd_message_member_array[2] = {
  {
    "l_speed",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(robot_interface__msg__DriveCmd, l_speed),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "r_speed",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(robot_interface__msg__DriveCmd, r_speed),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers robot_interface__msg__DriveCmd__rosidl_typesupport_introspection_c__DriveCmd_message_members = {
  "robot_interface__msg",  // message namespace
  "DriveCmd",  // message name
  2,  // number of fields
  sizeof(robot_interface__msg__DriveCmd),
  robot_interface__msg__DriveCmd__rosidl_typesupport_introspection_c__DriveCmd_message_member_array,  // message members
  robot_interface__msg__DriveCmd__rosidl_typesupport_introspection_c__DriveCmd_init_function,  // function to initialize message memory (memory has to be allocated)
  robot_interface__msg__DriveCmd__rosidl_typesupport_introspection_c__DriveCmd_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t robot_interface__msg__DriveCmd__rosidl_typesupport_introspection_c__DriveCmd_message_type_support_handle = {
  0,
  &robot_interface__msg__DriveCmd__rosidl_typesupport_introspection_c__DriveCmd_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_robot_interface
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, robot_interface, msg, DriveCmd)() {
  if (!robot_interface__msg__DriveCmd__rosidl_typesupport_introspection_c__DriveCmd_message_type_support_handle.typesupport_identifier) {
    robot_interface__msg__DriveCmd__rosidl_typesupport_introspection_c__DriveCmd_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &robot_interface__msg__DriveCmd__rosidl_typesupport_introspection_c__DriveCmd_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
