"use client";

import { authService } from "@/lib/auth";
import { useRouter } from "next/navigation";
import { useEffect } from "react";

export function withAuth<P extends object>(
  WrappedComponent: React.ComponentType<P>
) {
  return function ProtectedRoute(props: P) {
    const router = useRouter();

    useEffect(() => {
      if (!authService.isAuthenticated()) {
        router.replace("/auth/signin");
      }
    }, [router]);

    if (!authService.isAuthenticated()) {
      return null; // or a loading spinner
    }

    return <WrappedComponent {...props} />;
  };
}
