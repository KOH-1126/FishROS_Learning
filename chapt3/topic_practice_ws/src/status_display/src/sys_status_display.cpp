#include <QApplication>
#include <QGridLayout>
#include <QLabel>
#include <QProgressBar>
#include <QTimer>
#include <QVBoxLayout>
#include <QWidget>
#include <rclcpp/rclcpp.hpp>
#include <status_interfaces/msg/system_status.hpp>

using SystemStatus = status_interfaces::msg::SystemStatus;

class SystemStatusDisplay : public rclcpp::Node
{
public:
    explicit SystemStatusDisplay(QWidget &window) : Node("system_status_display")
    {
        window.setWindowTitle("FishROS | System Status");
        window.setMinimumSize(800, 510);
        window.setStyleSheet(
            "QWidget { background: #101c2d; color: #e5edf7; font-family: 'DejaVu Sans'; }"
            "QLabel { font-size: 15px; }"
            "QLabel#title { font-size: 30px; font-weight: bold; }"
            "QLabel#subtitle, QLabel#footer { color: #91a7bf; font-size: 13px; }"
            "QLabel#value { font-size: 19px; color: #66d9c5; padding: 9px; }"
            "QProgressBar { background: #24354a; border: 0; border-radius: 7px;"
            " height: 28px; text-align: center; color: white; }"
            "QProgressBar::chunk { background: #219c95; border-radius: 7px; }");
        auto *layout = new QVBoxLayout(&window);
        layout->setContentsMargins(34, 30, 34, 26);
        layout->setSpacing(17);
        auto *title = new QLabel("System Status");
        title->setObjectName("title");
        layout->addWidget(title);
        auto *subtitle = new QLabel("CHAPTER 03  /  ROS 2 TOPICS + QT");
        subtitle->setObjectName("subtitle");
        layout->addWidget(subtitle);
        auto *grid = new QGridLayout;
        grid->setHorizontalSpacing(28);
        grid->setVerticalSpacing(12);
        cpu_ = new QProgressBar;
        memory_ = new QProgressBar;
        grid->addWidget(new QLabel("CPU usage"), 0, 0);
        grid->addWidget(cpu_, 0, 1);
        grid->addWidget(new QLabel("Memory usage"), 1, 0);
        grid->addWidget(memory_, 1, 1);
        const QString names[] = {"Host", "Memory available / total", "Network sent / received"};
        QLabel **values[] = {&host_, &ram_, &network_};
        for (int i = 0; i < 3; ++i) {
            *values[i] = new QLabel("Waiting for publisher...");
            (*values[i])->setObjectName("value");
            grid->addWidget(new QLabel(names[i]), i + 2, 0);
            grid->addWidget(*values[i], i + 2, 1);
        }
        grid->setColumnStretch(1, 1);
        layout->addLayout(grid);
        layout->addStretch();
        footer_ = new QLabel("Topic: /system_status  |  Waiting for live data");
        footer_->setObjectName("footer");
        layout->addWidget(footer_);
        subscriber_ = create_subscription<SystemStatus>(
            "system_status", 10, [this](const SystemStatus::SharedPtr msg) {
                cpu_->setValue(qRound(msg->cpu_percent));
                memory_->setValue(qRound(msg->memory_percent));
                host_->setText(QString::fromStdString(msg->host_name));
                ram_->setText(QString("%1 / %2 MiB")
                    .arg(msg->memory_available, 0, 'f', 0).arg(msg->memory_total, 0, 'f', 0));
                network_->setText(QString("%1 / %2 MiB")
                    .arg(msg->net_sent, 0, 'f', 1).arg(msg->net_recv, 0, 'f', 1));
                footer_->setText(QString("Topic: /system_status  |  Live  |  ROS time: %1 s")
                    .arg(msg->stamp.sec));
            });
    }
private:
    QLabel *host_, *ram_, *network_, *footer_;
    QProgressBar *cpu_, *memory_;
    rclcpp::Subscription<SystemStatus>::SharedPtr subscriber_;
};

int main(int argc, char *argv[])
{
    rclcpp::init(argc, argv);
    QApplication app(argc, argv);
    QWidget window;
    auto node = std::make_shared<SystemStatusDisplay>(window);
    // Keep ROS callbacks on the Qt thread so widget updates are thread-safe.
    QTimer timer;
    QObject::connect(&timer, &QTimer::timeout, [&]() {
        if (rclcpp::ok()) {
            rclcpp::spin_some(node);
        } else {
            app.quit();
        }
    });
    timer.start(50);
    window.show();
    const int result = app.exec();
    rclcpp::shutdown();
    return result;
}
