/**********************************************
 * Self-Driving Car Nano-degree - Udacity
 *  Created on: December 11, 2020
 *      Author: Mathilde Badoual
 **********************************************/

#include "pid_controller.h"
#include <vector>
#include <iostream>
#include <math.h>

using namespace std;

PID::PID(double Kp, double Ki, double Kd, float output_lim_max, float output_lim_min) {
   Init(Kp, Ki, Kd, output_lim_max, output_lim_min);
   InitTwiddle();
}

PID::~PID() {}

void PID::Init(double Kpi, double Kii, double Kdi, float output_lim_maxi, float output_lim_mini) {
   /**
   * TODO: Initialize PID coefficients (and errors, if needed)
   **/
  this->Kp = Kpi;
  this->Ki = Kii;
  this->Kd = Kdi;
  this->output_lim_max = output_lim_maxi;
  this->output_lim_min = output_lim_mini;
}

void PID::UpdateError(double cte) {
   /**
   * TODO: Update PID errors based on cte.
   **/
  this->cte_old = this->cte;
  this->cte = cte;
  this->diff_cte = this->cte - this->cte_old;
  this->int_cte += this->cte;
}

double PID::TotalError() {
   /**
   * TODO: Calculate and return the total error
    * The code should return a value in the interval [output_lim_mini, output_lim_maxi]
   */
    double control;

    control = (-this->Kp * this->cte) - (this->Kd * this->diff_cte) - (this->Ki * this->int_cte);
    this->n++;

    if (control > this->output_lim_max)
      control = this->output_lim_max;
    else if (control < output_lim_min)
      control = output_lim_min;
      
    return control;
}

double PID::UpdateDeltaTime(double new_delta_time) {
   /**
   * TODO: Update the delta time with new value
   */
  this->new_delta_time = new_delta_time;
}

void PID::InitTwiddle(void) {
  for (unsigned int i = 0; i < 3; i++) {
    this->p.push_back(0.0);
    this->dp.push_back(1.0);
  }
}

int PID::Twiddle(double cte) {
  if (this->n > 20) 
  {
    auto best_err = this->TotalError();

    while ((this->dp[0] + this->dp[1] + this->dp[2]) > cte) 
    {
       if ((this->n) %100 == 0)
       {
          std::cout <<"dp values " << this->p[0] << " " << this->p[1] << " " << this->p[2];
       }
      for (unsigned int i = 0; i < 3; i++) {
        auto err = this->TotalError();
        this->p[i] += this->dp[i];

        if (err < best_err) {
          best_err = err;
          this->dp[i] *= 1.1;
        } else {
          this->p[i] -= 2 * this->dp[i];
          err = this->TotalError();

          if (err < best_err) {
            best_err = err;
            dp[i] *= 1.1;
          } else {
            this->p[i] += this->dp[i];
            this->dp[i] *= 0.9;
          }
        }
      }
    }
    std::cout <<"dp values " << this->p[0] << " " << this->p[1] << " " << this->p[2];
  }
  return 0;
}