// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from robot_interface:msg/DriveCmd.idl
// generated code does not contain a copyright notice
#include "robot_interface/msg/detail/drive_cmd__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


bool
robot_interface__msg__DriveCmd__init(robot_interface__msg__DriveCmd * msg)
{
  if (!msg) {
    return false;
  }
  // l_speed
  // r_speed
  return true;
}

void
robot_interface__msg__DriveCmd__fini(robot_interface__msg__DriveCmd * msg)
{
  if (!msg) {
    return;
  }
  // l_speed
  // r_speed
}

bool
robot_interface__msg__DriveCmd__are_equal(const robot_interface__msg__DriveCmd * lhs, const robot_interface__msg__DriveCmd * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // l_speed
  if (lhs->l_speed != rhs->l_speed) {
    return false;
  }
  // r_speed
  if (lhs->r_speed != rhs->r_speed) {
    return false;
  }
  return true;
}

bool
robot_interface__msg__DriveCmd__copy(
  const robot_interface__msg__DriveCmd * input,
  robot_interface__msg__DriveCmd * output)
{
  if (!input || !output) {
    return false;
  }
  // l_speed
  output->l_speed = input->l_speed;
  // r_speed
  output->r_speed = input->r_speed;
  return true;
}

robot_interface__msg__DriveCmd *
robot_interface__msg__DriveCmd__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  robot_interface__msg__DriveCmd * msg = (robot_interface__msg__DriveCmd *)allocator.allocate(sizeof(robot_interface__msg__DriveCmd), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(robot_interface__msg__DriveCmd));
  bool success = robot_interface__msg__DriveCmd__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
robot_interface__msg__DriveCmd__destroy(robot_interface__msg__DriveCmd * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    robot_interface__msg__DriveCmd__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
robot_interface__msg__DriveCmd__Sequence__init(robot_interface__msg__DriveCmd__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  robot_interface__msg__DriveCmd * data = NULL;

  if (size) {
    data = (robot_interface__msg__DriveCmd *)allocator.zero_allocate(size, sizeof(robot_interface__msg__DriveCmd), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = robot_interface__msg__DriveCmd__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        robot_interface__msg__DriveCmd__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
robot_interface__msg__DriveCmd__Sequence__fini(robot_interface__msg__DriveCmd__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      robot_interface__msg__DriveCmd__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

robot_interface__msg__DriveCmd__Sequence *
robot_interface__msg__DriveCmd__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  robot_interface__msg__DriveCmd__Sequence * array = (robot_interface__msg__DriveCmd__Sequence *)allocator.allocate(sizeof(robot_interface__msg__DriveCmd__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = robot_interface__msg__DriveCmd__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
robot_interface__msg__DriveCmd__Sequence__destroy(robot_interface__msg__DriveCmd__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    robot_interface__msg__DriveCmd__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
robot_interface__msg__DriveCmd__Sequence__are_equal(const robot_interface__msg__DriveCmd__Sequence * lhs, const robot_interface__msg__DriveCmd__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!robot_interface__msg__DriveCmd__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
robot_interface__msg__DriveCmd__Sequence__copy(
  const robot_interface__msg__DriveCmd__Sequence * input,
  robot_interface__msg__DriveCmd__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(robot_interface__msg__DriveCmd);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    robot_interface__msg__DriveCmd * data =
      (robot_interface__msg__DriveCmd *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!robot_interface__msg__DriveCmd__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          robot_interface__msg__DriveCmd__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!robot_interface__msg__DriveCmd__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
