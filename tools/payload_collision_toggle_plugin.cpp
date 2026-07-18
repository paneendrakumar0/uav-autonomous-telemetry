#include <gazebo/gazebo.hh>
#include <gazebo/physics/physics.hh>
#include <gazebo/common/common.hh>

namespace gazebo
{
  class PayloadCollisionTogglePlugin : public ModelPlugin
  {
    public: void Load(physics::ModelPtr _parent, sdf::ElementPtr _sdf)
    {
      this->model = _parent;
      this->updateConnection = event::Events::ConnectWorldUpdateBegin(
          std::bind(&PayloadCollisionTogglePlugin::OnUpdate, this));
      
      this->payload_link = this->model->GetLink("slung_payload");
      if (!this->payload_link) {
        gzerr << "PayloadCollisionTogglePlugin: slung_payload link not found!\n";
        return;
      }
      gzmsg << "PayloadCollisionTogglePlugin loaded successfully.\n";
    }

    public: void OnUpdate()
    {
      if (!this->payload_link) return;
      
      // Get the Z position of the model (base_link)
      double z = this->model->WorldPose().Pos().Z();
      
      // Enable collision if Z > 1.0, else disable
      bool should_collide = (z > 1.0);
      
      if (should_collide != this->is_collision_enabled) {
        // We must loop through all collisions in the link and enable/disable them
        auto collisions = this->payload_link->GetCollisions();
        for (auto &col : collisions) {
          if (should_collide) {
            col->SetCollideBits(0xFFFFFFFF);
            col->SetCategoryBits(0xFFFFFFFF);
          } else {
            col->SetCollideBits(0x00000000);
            col->SetCategoryBits(0x00000000);
          }
        }
        this->is_collision_enabled = should_collide;
        gzmsg << "PayloadCollisionTogglePlugin: Collision is now " << (should_collide ? "ON" : "OFF") << " at Z=" << z << "\n";
      }
    }

    private: physics::ModelPtr model;
    private: physics::LinkPtr payload_link;
    private: event::ConnectionPtr updateConnection;
    private: bool is_collision_enabled = true; // Assume true initially so it turns off immediately
  };

  GZ_REGISTER_MODEL_PLUGIN(PayloadCollisionTogglePlugin)
}
