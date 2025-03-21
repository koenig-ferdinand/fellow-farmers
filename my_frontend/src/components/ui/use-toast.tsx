// src/components/ui/use-toast.tsx
import { useCallback } from "react";

interface ToastOptions {
  title: string;
  description?: string;
  variant?: "default" | "destructive";
}

export function useToast() {
  const toast = useCallback((options: ToastOptions) => {
    // For now, just log them
    console.log("Toast:", options.title, "-", options.description);
  }, []);

  return { toast };
}
