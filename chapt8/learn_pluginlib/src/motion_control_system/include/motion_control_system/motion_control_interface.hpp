#ifndef MOTION_CONTROL_INTERFACE_HPP
#define MOTION_CONTROL_INTERFACE_HPP

namespace motion_control_system{
    class MotionController{
        private:
            // Private members and methods can be defined here
        public:
            virtual void start() = 0; // Pure virtual function to start the motion controller
            virtual void stop() = 0;  // Pure virtual function to stop the motion controller
    };
}

#endif // MOTION_CONTROL_INTERFACE_HPP