/* SPDX-License-Identifier: GPL-3.0-or-later */
#pragma once
#include <deko3d.hpp>
#include <memory>
#include <string>

/* Borrows the renderer's device and command queue. The caller drains the
 * queue before destroying this object. All GPU resources are preallocated;
 * record() never compiles, allocates, waits or submits commands. */
class NativeLsfg {
public:
  static std::unique_ptr<NativeLsfg> prepare(bool performance, unsigned flow_denominator,
      const char *dll_path, const char *cache_root, std::string &error);
  bool initializeGpu(DkDevice device, unsigned width, unsigned height, std::string &error);
  ~NativeLsfg();
  const dk::Image *input() const;
  bool record(DkCmdBuf cmd, const dk::Image *&generated,
              const dk::Image *&original, std::string &error);
  void reset();
private:
  struct State;
  explicit NativeLsfg(std::unique_ptr<State> state);
  std::unique_ptr<State> state_;
};
