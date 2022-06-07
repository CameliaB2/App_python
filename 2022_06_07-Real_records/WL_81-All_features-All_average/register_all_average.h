/*
 ******************************************************************************
 * @file    register_all_average.h
 * @author  Sensors Software Solution Team
 * @brief   This file contains the configuration for register_all_average.
 *
 ******************************************************************************
 * @attention
 *
 * <h2><center>&copy; Copyright (c) 2021 STMicroelectronics.
 * All rights reserved.</center></h2>
 *
 * This software component is licensed by ST under BSD 3-Clause license,
 * the "License"; You may not use this file except in compliance with the
 * License. You may obtain a copy of the License at:
 *                        opensource.org/licenses/BSD-3-Clause
 *
 */

/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef REGISTER_ALL_AVERAGE_H
#define REGISTER_ALL_AVERAGE_H

#ifdef __cplusplus
  extern "C" {
#endif

/* Includes ------------------------------------------------------------------*/
#include <stdint.h>
#ifndef MEMS_UCF_SHARED_TYPES
#define MEMS_UCF_SHARED_TYPES

/** Common data block definition **/
typedef struct {
  uint8_t address;
  uint8_t data;
} ucf_line_t;

#endif /* MEMS_UCF_SHARED_TYPES */

/** Configuration array generated from Unico Tool **/
const ucf_line_t register_all_average[] = {
  {.address = 0x10, .data = 0x00,},
  {.address = 0x11, .data = 0x00,},
  {.address = 0x01, .data = 0x80,},
  {.address = 0x04, .data = 0x00,},
  {.address = 0x05, .data = 0x00,},
  {.address = 0x17, .data = 0x40,},
  {.address = 0x02, .data = 0x11,},
  {.address = 0x08, .data = 0xEA,},
  {.address = 0x09, .data = 0xE8,},
  {.address = 0x09, .data = 0x03,},
  {.address = 0x09, .data = 0xFC,},
  {.address = 0x09, .data = 0x03,},
  {.address = 0x09, .data = 0x01,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0x14,},
  {.address = 0x02, .data = 0x11,},
  {.address = 0x08, .data = 0xF2,},
  {.address = 0x09, .data = 0x51,},
  {.address = 0x02, .data = 0x11,},
  {.address = 0x08, .data = 0xFA,},
  {.address = 0x09, .data = 0x3C,},
  {.address = 0x09, .data = 0x03,},
  {.address = 0x09, .data = 0x38,},
  {.address = 0x09, .data = 0x04,},
  {.address = 0x09, .data = 0x44,},
  {.address = 0x09, .data = 0x04,},
  {.address = 0x02, .data = 0x31,},
  {.address = 0x08, .data = 0x3C,},
  {.address = 0x09, .data = 0x3F,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0x04,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0x08,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0x0C,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0x18,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0x1C,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0x20,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0x01,},
  {.address = 0x09, .data = 0x04,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0x01,},
  {.address = 0x09, .data = 0x08,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0x01,},
  {.address = 0x09, .data = 0x0C,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0x01,},
  {.address = 0x09, .data = 0x18,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0x01,},
  {.address = 0x09, .data = 0x1C,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0x01,},
  {.address = 0x09, .data = 0x20,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0x03,},
  {.address = 0x09, .data = 0x04,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0xFC,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0x7C,},
  {.address = 0x09, .data = 0x03,},
  {.address = 0x09, .data = 0x08,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0xFC,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0x7C,},
  {.address = 0x09, .data = 0x03,},
  {.address = 0x09, .data = 0x0C,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0xFC,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0x7C,},
  {.address = 0x09, .data = 0x03,},
  {.address = 0x09, .data = 0x18,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0xFC,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0x7C,},
  {.address = 0x09, .data = 0x03,},
  {.address = 0x09, .data = 0x1C,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0xFC,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0x7C,},
  {.address = 0x09, .data = 0x03,},
  {.address = 0x09, .data = 0x20,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0xFC,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0x7C,},
  {.address = 0x09, .data = 0x10,},
  {.address = 0x09, .data = 0x04,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0xFC,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0x7C,},
  {.address = 0x09, .data = 0x10,},
  {.address = 0x09, .data = 0x08,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0xFC,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0x7C,},
  {.address = 0x09, .data = 0x10,},
  {.address = 0x09, .data = 0x0C,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0xFC,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0x7C,},
  {.address = 0x09, .data = 0x10,},
  {.address = 0x09, .data = 0x18,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0xFC,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0x7C,},
  {.address = 0x09, .data = 0x10,},
  {.address = 0x09, .data = 0x1C,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0xFC,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0x7C,},
  {.address = 0x09, .data = 0x10,},
  {.address = 0x09, .data = 0x20,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0xFC,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0x7C,},
  {.address = 0x09, .data = 0x11,},
  {.address = 0x09, .data = 0x04,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0xFC,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0x7C,},
  {.address = 0x09, .data = 0x11,},
  {.address = 0x09, .data = 0x08,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0xFC,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0x7C,},
  {.address = 0x09, .data = 0x11,},
  {.address = 0x09, .data = 0x0C,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0xFC,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0x7C,},
  {.address = 0x09, .data = 0x11,},
  {.address = 0x09, .data = 0x18,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0xFC,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0x7C,},
  {.address = 0x09, .data = 0x11,},
  {.address = 0x09, .data = 0x1C,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0xFC,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0x7C,},
  {.address = 0x09, .data = 0x11,},
  {.address = 0x09, .data = 0x20,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0xFC,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0x7C,},
  {.address = 0x09, .data = 0x1F,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x02, .data = 0x41,},
  {.address = 0x08, .data = 0x38,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x01, .data = 0x00,},
  {.address = 0x01, .data = 0x80,},
  {.address = 0x17, .data = 0x40,},
  {.address = 0x02, .data = 0x41,},
  {.address = 0x08, .data = 0x44,},
  {.address = 0x09, .data = 0xD8,},
  {.address = 0x09, .data = 0x2E,},
  {.address = 0x09, .data = 0x03,},
  {.address = 0x09, .data = 0x8E,},
  {.address = 0x09, .data = 0xCE,},
  {.address = 0x09, .data = 0x9E,},
  {.address = 0x09, .data = 0x24,},
  {.address = 0x09, .data = 0xC0,},
  {.address = 0x09, .data = 0x22,},
  {.address = 0x09, .data = 0x25,},
  {.address = 0x09, .data = 0x80,},
  {.address = 0x09, .data = 0xE5,},
  {.address = 0x09, .data = 0x5E,},
  {.address = 0x09, .data = 0x31,},
  {.address = 0x09, .data = 0x0A,},
  {.address = 0x09, .data = 0x8B,},
  {.address = 0x09, .data = 0x86,},
  {.address = 0x09, .data = 0x39,},
  {.address = 0x09, .data = 0x06,},
  {.address = 0x09, .data = 0x94,},
  {.address = 0x09, .data = 0x8A,},
  {.address = 0x09, .data = 0x12,},
  {.address = 0x09, .data = 0x8C,},
  {.address = 0x09, .data = 0xE1,},
  {.address = 0x09, .data = 0x13,},
  {.address = 0x09, .data = 0xAE,},
  {.address = 0x09, .data = 0x09,},
  {.address = 0x09, .data = 0x92,},
  {.address = 0x09, .data = 0x30,},
  {.address = 0x09, .data = 0x28,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0xA6,},
  {.address = 0x09, .data = 0x9F,},
  {.address = 0x09, .data = 0xBB,},
  {.address = 0x09, .data = 0x80,},
  {.address = 0x09, .data = 0xF7,},
  {.address = 0x09, .data = 0x0A,},
  {.address = 0x09, .data = 0x10,},
  {.address = 0x09, .data = 0x0C,},
  {.address = 0x09, .data = 0xE5,},
  {.address = 0x09, .data = 0x21,},
  {.address = 0x09, .data = 0x30,},
  {.address = 0x09, .data = 0x0C,},
  {.address = 0x09, .data = 0x99,},
  {.address = 0x09, .data = 0x6D,},
  {.address = 0x09, .data = 0x27,},
  {.address = 0x09, .data = 0x08,},
  {.address = 0x09, .data = 0xE6,},
  {.address = 0x09, .data = 0x70,},
  {.address = 0x09, .data = 0x30,},
  {.address = 0x09, .data = 0x00,},
  {.address = 0x09, .data = 0xA3,},
  {.address = 0x09, .data = 0x8C,},
  {.address = 0x09, .data = 0x9C,},
  {.address = 0x09, .data = 0x8C,},
  {.address = 0x09, .data = 0xE3,},
  {.address = 0x01, .data = 0x80,},
  {.address = 0x17, .data = 0x00,},
  {.address = 0x04, .data = 0x00,},
  {.address = 0x05, .data = 0x10,},
  {.address = 0x02, .data = 0x01,},
  {.address = 0x01, .data = 0x00,},
  {.address = 0x5E, .data = 0x02,},
  {.address = 0x01, .data = 0x80,},
  {.address = 0x0D, .data = 0x01,},
  {.address = 0x60, .data = 0x15,},
  {.address = 0x01, .data = 0x00,},
  {.address = 0x10, .data = 0x20,},
  {.address = 0x11, .data = 0x2C,}
};

#ifdef __cplusplus
}
#endif

#endif /* REGISTER_ALL_AVERAGE_H */

