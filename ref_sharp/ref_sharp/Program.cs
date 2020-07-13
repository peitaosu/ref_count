using Microsoft.Win32;
using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ref_sharp
{
    class ReferenceManager
    {
        private string msi_key_string = "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Installer\\UserData\\S-1-5-18\\Components\\";
        private Config config = new Config();

        public void LoadConfig(string config_file = "ref.conf")
        {
            using (StreamReader r = new StreamReader(config_file))
            {
                string json = r.ReadToEnd();
                this.config = JsonConvert.DeserializeObject<Config>(json);
            }
        }
        public bool Install()
        {
            try
            {
                this.AddReferences();
                return true;
            }
            catch
            {
                return false;
            }
        }
        public bool Uninstall()
        {
            try
            {
                this.ReduceReferences();
                return true;
            }
            catch
            {
                return false;
            }
        }

        public void AddReferences()
        {
            foreach(KeyValuePair<string, Reference> reference in this.config.References)
            {
                this._add_count_in_registry(reference.Key, this.config.ProductCode, reference.Value.File);
            }

        }
        public void ReduceReferences()
        {
            foreach (KeyValuePair<string, Reference> reference in this.config.References)
            {
                if(this._reduce_count_in_registry(reference.Key, this.config.ProductCode) == 0)
                    this._remove_file(reference);
            }
        }

        private void _remove_file(KeyValuePair<string, Reference> reference)
        {
            string file = reference.Value.File;
            if (File.Exists(file))
                File.Delete(file);
        }
        private string _reverse(string input)
        {
            char[] array = input.ToCharArray();
            Array.Reverse(array);
            return new string(array);
        }

        private string _format_guid(string guid)
        {
            return this._reverse(guid.Substring(1, 8)) + this._reverse(guid.Substring(10, 4)) + this._reverse(guid.Substring(15, 2)) + this._reverse(guid.Substring(17, 2)) + this._reverse(guid.Substring(20, 2)) + this._reverse(guid.Substring(22, 2)) + this._reverse(guid.Substring(25, 2)) + this._reverse(guid.Substring(27, 2)) + this._reverse(guid.Substring(29, 2)) + this._reverse(guid.Substring(31, 2)) + this._reverse(guid.Substring(33, 2)) + this._reverse(guid.Substring(35, 2));
        }

        private bool _add_count_in_registry(string component, string product, string file)
        {
            RegistryKey component_key = Registry.LocalMachine.OpenSubKey(msi_key_string + this._format_guid(component), true);
            if (component_key == null)
            {
                component_key = Registry.LocalMachine.CreateSubKey(msi_key_string + this._format_guid(component));
            }
            component_key.SetValue(this._format_guid(product), file);
            component_key.Close();
            return true;
        }

        private int _reduce_count_in_registry(string component, string product)
        {
            RegistryKey component_key = Registry.LocalMachine.OpenSubKey(msi_key_string + this._format_guid(component), true);
            if (component_key.GetValue(this._format_guid(product)) != null)
                component_key.DeleteValue(this._format_guid(product));
            int remain_count = component_key.ValueCount;
            component_key.Close();
            return remain_count;
        }

        private int _get_count_in_registry(string component)
        {
            RegistryKey component_key = Registry.LocalMachine.OpenSubKey(msi_key_string + this._format_guid(component), true);
            if(component_key != null)
                return component_key.ValueCount;
            return 0;
        }

        private bool _delete_count_in_registry(string component, string product)
        {
            RegistryKey component_key = Registry.LocalMachine.OpenSubKey(msi_key_string + this._format_guid(component), true);
            if (component_key != null && component_key.GetValue(this._format_guid(product)) != null)
            {
                component_key.DeleteValue(this._format_guid(product));
                component_key.Close();
            }
            return true;
        }

        private RegistryKey _get_registry_root(string registry_key)
        {
            switch (registry_key)
            {
                case "HKEY_LOCAL_MACHINE":
                    return Registry.LocalMachine;
                case "HKEY_CURRENT_USER":
                    return Registry.CurrentUser;
                default:
                    return Registry.LocalMachine;
            }
        }

        private string _get_knownfolderid(string folder)
        {
            switch(folder)
            {
                case "ProgramFilesX64":
                    return Environment.GetFolderPath(Environment.SpecialFolder.ProgramFiles);
                case "ProgramFilesX86":
                    return Environment.GetFolderPath(Environment.SpecialFolder.ProgramFilesX86);
                case "CommonProgramFilesX64":
                    return Environment.GetFolderPath(Environment.SpecialFolder.CommonProgramFiles);
                case "CommonProgramFilesX86":
                    return Environment.GetFolderPath(Environment.SpecialFolder.CommonProgramFilesX86);
                case "AppData":
                    return Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData);
                case "Local AppData":
                    return Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData);
                case "CommonAppData":
                    return Environment.GetFolderPath(Environment.SpecialFolder.CommonApplicationData);
                default:
                    return null;
            }
        }

}

class Config
    {
        [JsonProperty("ProductCode")]
        public string ProductCode;
        [JsonProperty("References")]
        public Dictionary<string, Reference> References;
    }
    class Reference
    {
        [JsonProperty("File")]
        public string File;
        [JsonProperty("Registry")]
        public Dictionary<string, List<string>> Registry;
    }

    class Program
    {
        static void Main(string[] args)
        {
            ReferenceManager refman = new ReferenceManager();
            refman.LoadConfig(args[0]);
            var install_watch = System.Diagnostics.Stopwatch.StartNew();
            refman.Install();
            install_watch.Stop();
            var install_elapsed_ms = install_watch.ElapsedMilliseconds;
            var uninstall_watch = System.Diagnostics.Stopwatch.StartNew();
            refman.Uninstall();
            uninstall_watch.Stop();
            var uninstall_elapsed_ms = uninstall_watch.ElapsedMilliseconds;
        }
    }
}
