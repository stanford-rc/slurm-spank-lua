-- ===========================================================================
-- SPANK plugin to demonstrate when and where and by whom the SPANK functions 
-- are called.
-- ===========================================================================

--
-- includes
--

local posix = require("posix")


-- 
-- constants
--

myname = "spank_demo"


--
-- functions
--

function gethostname()
    local f = io.popen ("/bin/hostname")
    local hostname = f:read("*a") or ""
    f:close()
    hostname = string.gsub(hostname, "\n$", "")
    return hostname
end

function getuid()
    local f = io.popen ("/bin/id -un")
    local uid = f:read("*a") or ""
    f:close()
    uid = string.gsub(uid, "\n$", "")
    return uid
end

function getgid()
    local f = io.popen ("/bin/id -gn")
    local gid = f:read("*a") or ""
    f:close()
    gid = string.gsub(gid, "\n$", "")
    return gid
end

function display_msg(spank, caller)
    local context = spank.context
    local hostname = gethostname()
    local uid = getuid()
    local gid = getgid()

    SPANK.log_info("%s: ctx:%s host:%s caller:%s uid:%s gid:%s" , myname, context, hostname, caller, uid, gid)
    return 0
end


--
-- SPANK functions
-- cf. https://slurm.schedmd.com/spank.html
--

function slurm_spank_init (spank)
    display_msg(spank, "slurm_spank_init")
    return 0
end

function slurm_spank_slurmd_init (spank)
    display_msg(spank, "slurm_spank_slurmd_init")
    return 0
end

function slurm_spank_init_post_opt (spank)
    display_msg(spank, "slurm_spank_init_post_opt")
    return 0
end

function slurm_spank_local_user_init (spank)
    display_msg(spank, "slurm_spank_local_user_init")
    return 0
end

function slurm_spank_user_init (spank)
    display_msg(spank, "slurm_spank_user_init")
    return 0
end

function slurm_spank_task_init_privileged (spank)
    display_msg(spank, "slurm_spank_task_init_privileged")
    return 0
end

function slurm_spank_task_init (spank)
    display_msg(spank, "slurm_spank_task_init")
    return 0
end

function slurm_spank_task_post_fork (spank)
    display_msg(spank, "slurm_spank_task_post_fork")
    return 0
end

function slurm_spank_task_exit (spank)
    display_msg(spank, "slurm_spank_task_exit")
    return 0
end

function slurm_spank_exit (spank)
    display_msg(spank, "slurm_spank_exit")
    return 0
end

function slurm_spank_job_epilog (spank)
    display_msg(spank, "slurm_spank_job_epilog")
    return 0
end

function slurm_spank_slurmd_exit (spank)
    display_msg(spank, "slurm_spank_slurmd_exit")
    return 0
end
