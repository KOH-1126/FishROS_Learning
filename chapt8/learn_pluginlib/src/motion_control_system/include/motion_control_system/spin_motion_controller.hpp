#ifndef SPIN_MOTION_CONTROLLER_HPP
#define SPIN_MOTION_CONTROLLER_HPP
#include "motion_control_interface.hpp"

namespace motion_control_system{
    class SpinMotionController: public MotionController{
        private:
            // Private members and methods can be defined here
        public:
            void start() override; 
            void stop() override;  
    };
}

#endif // SPIN_CONTROLLER_MOTION_HPP