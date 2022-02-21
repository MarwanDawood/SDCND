/**********************************************
 * Self-Driving Car Nano-degree - Udacity
 *  Created on: December 11, 2020
 *      Author: Mathilde Badoual
 **********************************************/

#ifndef PID_CONTROLLER_H
#define PID_CONTROLLER_H

#include <vector>

using namespace std;

class PID {
private:

   /**
   * TODO: Create the PID class
   **/

    /*
    * Errors
    */
    double cte = 0;
    double cte_old = 0;
    double diff_cte = 0;
    double int_cte = 0;

    /*
    * Coefficients
    */
    double Kp;
    double Ki;
    double Kd;

    vector<double> p;
    vector<double> dp;
    int n = 0;

    /*
    * Output limits
    */
    double output_lim_max;
    double output_lim_min;

    /*
    * Delta time
    */
    double new_delta_time;

    /*
    * Initialize PID.
    */
    void Init(double Kp, double Ki, double Kd, float output_lim_max, float output_lim_min);

public:
    /*
    * Constructor
    */
    PID(double Kp, double Ki, double Kd, float output_lim_max, float output_lim_min);

    /*
    * Destructor.
    */
    virtual ~PID();

    /*
    * Update the PID error variables given cross track error.
    */
    void UpdateError(double cte);

    /*
    * Calculate the total PID error.
    */
    double TotalError();
  
    /*
    * Update the delta time.
    */
    double UpdateDeltaTime(double new_delta_time);

    /* Twiddle */
    void InitTwiddle(void);
    int Twiddle(double cte);
};

#endif //PID_CONTROLLER_H


