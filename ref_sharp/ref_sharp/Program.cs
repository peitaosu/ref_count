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
            return true;
        }
        public bool Uninstall()
        {
            return true;
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
                this._reduce_count_in_registry(reference.Key, this.config.ProductCode);
            }
        }
        private bool _add_count_in_registry(string component, string product, string file)
        {
            RegistryKey component_key = Registry.LocalMachine.OpenSubKey(msi_key_string + component, true);
            if (component_key == null)
            {
                component_key = Registry.LocalMachine.CreateSubKey(msi_key_string + component);
            }
            component_key.SetValue(product, file);
            component_key.Close();
            return true;
        }

        private bool _reduce_count_in_registry(string component, string product)
        {
            RegistryKey component_key = Registry.LocalMachine.OpenSubKey(msi_key_string + component, true);
            if (component_key.GetValue(product) != null)
                component_key.DeleteValue(product);
            component_key.Close();
            return true;
        }

        private int _get_count_in_registry(string component)
        {
            RegistryKey component_key = Registry.LocalMachine.OpenSubKey(msi_key_string + component, true);
            if(component_key != null)
                return component_key.ValueCount;
            return 0;
        }

        private bool _delete_count_in_registry(string component, string product)
        {
            RegistryKey component_key = Registry.LocalMachine.OpenSubKey(msi_key_string + component, true);
            if (component_key != null && component_key.GetValue(product) != null)
            {
                component_key.DeleteValue(product);
                component_key.Close();
            }
            return true;
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
