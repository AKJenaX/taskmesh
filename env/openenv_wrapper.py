from env.taskmesh_env import TaskMeshEnv

class OpenEnvTaskMesh:

    def __init__(self):
        self.env = TaskMeshEnv()

    def reset(self):
        return self.env.reset()

    def step(self, action):
        result = self.env.step(action)

        if isinstance(result, tuple) and len(result) == 3:
            state, reward, done = result
            info = {}
        else:
            state, reward, done, info = result

        if info is None:
            info = {}

        if hasattr(self.env, "tasks"):
            try:
                info["remaining_tasks"] = len(self.env.tasks)
            except:
                pass

        return state, reward, done, info

    def render(self):
        try:
            print(self.env.tasks)
        except:
            pass
